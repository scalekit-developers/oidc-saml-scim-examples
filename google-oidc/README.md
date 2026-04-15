# Google OIDC Login Demo App

This is an app to understand how to configure Google OIDC for login with PKCE, JWKS verification, and discovery-based configuration. This is built using Python and Flask using [AuthLib](https://authlib.org/).

## Features

- **Authorization Code Flow with PKCE**: Secure OAuth 2.0 flow with Proof Key for Code Exchange
- **Discovery-based Configuration**: Automatically loads endpoints from Google's discovery document
- **JWKS Verification**: ID tokens are validated using Google's JSON Web Key Set
- **State Parameter Protection**: CSRF protection via random state validation
- **Secure Session Handling**: User claims stored in server-side sessions

## Prerequisites

- Python 3.8+
- Google Cloud project with OAuth 2.0 credentials configured

## Install

Install the required dependencies:

    $ pip install -r requirements.txt

## Configuration Steps

### Step 1: Create a Project in Google Cloud Console

Open the [Google Cloud Console](https://console.cloud.google.com) and create/select a project for OIDC authentication.

### Step 2: Configure the OAuth Consent Screen

Before you can use OIDC, Google requires you to configure the OAuth consent screen.
Navigate to: **APIs & Services → OAuth consent screen**

1. Choose "External" unless you're using a Google Workspace org
2. Add the required fields (app name, user support email, etc.)
3. Save and continue through scopes and test users

### Step 3: Create OAuth Client Credentials (OIDC App)

Create the OAuth 2.0 Client that your Flask app will use.
Go to: **APIs & Services → Credentials → Create Credentials → OAuth Client ID**

1. Choose "Web Application" and give it a name (e.g., Google OIDC Demo)
2. Add Authorized redirect URIs, specifically: `http://127.0.0.1:5000/callback`
3. Save and note your **Client ID** and **Client Secret**

### Step 4: Set Environment Variables

Create a `.env` file in the google-oidc directory:

```bash
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
FLASK_DEBUG=0
```

Load the environment variables:

    $ export $(cat .env | xargs)

Or on Windows PowerShell:

    $ Get-Content .env | ForEach-Object { $key, $value = $_ -split '='; [System.Environment]::SetEnvironmentVariable($key, $value) }

## Run

Start the server:

    $ export FLASK_APP=app.py
    $ flask run

Then visit:

    http://127.0.0.1:5000/

## Testing the Flow

1. Click "Login with Google" button
2. You'll be redirected to Google's login page
3. Complete authentication with your Google account
4. Accept the consent screen
5. You'll be redirected back to the app and see your profile with:
   - Full Name
   - First Name
   - Last Name
   - Email
   - Profile Picture

## How It Works

1. **Login Route** (`/login`): Generates state and PKCE parameters, then redirects to Google's authorization endpoint
2. **Callback Route** (`/callback`): Exchanges the authorization code for tokens, validates the ID token using JWKS, and stores claims
3. **Profile Route** (`/profile`): Displays authenticated user information
4. **Logout Route** (`/logout`): Clears the session

## Architecture Highlights

- **Discovery Document**: Fetches Google's OIDC metadata dynamically
- **PKCE Protection**: Each login session gets a unique code verifier and challenge
- **Token Validation**: ID tokens are verified using JWKS keys with issuer and audience checks
- **Stateless Design**: Ready for horizontal scaling (sessions can be moved to Redis)

## Security Considerations

- Always use `https://` in production (redirect URIs must match exactly)
- Keep `FLASK_DEBUG=0` in production
- Use secure, HttpOnly cookies (Flask default for session handling)
- Implement rate limiting on `/login` endpoint for production
- Add logging for security audits and debugging