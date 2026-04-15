# Firebase SAML SSO Demo

A demonstration of SAML Single Sign-On (SSO) integration using Firebase Authentication, Flask, and Okta as the Identity Provider (IdP). This application showcases how to implement SAML-based authentication in a web application.

## Authentication Flow

1. User clicks "Sign in with SSO" on the application
2. Firebase initiates SAML authentication request
3. User is redirected to Okta for authentication
4. Okta validates user credentials
5. Okta sends SAML response to Firebase
6. Firebase validates SAML response and creates/updates user
7. Application receives Firebase token
8. Backend verifies token and creates user session
9. User is logged in to the application

## Prerequisites

- Python 3.8+
- Firebase project with SAML Authentication enabled
- Okta account with SAML application configured
- Firebase service account credentials

## Project Structure

```
firebase-saml-demo/
├── app.py                 # Flask application
├── static/
│   ├── css/
│   │   └── styles.css    # Application styles
│   └── js/
│       ├── firebase-config.js  # Firebase initialization
│       └── auth.js       # Authentication logic
├── templates/
│   └── index.html        # Main application template
└── requirements.txt      # Python dependencies
```

## Configuration

### Firebase Setup

1. Create a Firebase project
2. Enable SAML authentication provider
3. Configure SAML provider with Okta settings:

   ```
    Entity ID: https://your-firebase-project-id.firebaseapp.com
    ACS URL: https://your-firebase-project-id.firebaseapp.com/__/auth/handler
   ```

### Okta Setup

1. Create a SAML application and assign a user to it.
2. Configure with Firebase URLs:

   ```
    Single sign-on URL: https://your-firebase-project-id.firebaseapp.com/__/auth/handler
    Audience URI: https://your-firebase-project-id.firebaseapp.com
   ```

## Installation

1. Clone the repository

    ```bash
    git clone <repository-url>
    cd firebase-okta
    ```

2. Create and activate virtual environment

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

4. Create environment file

    ```bash
    cp .env.template .env
    # Edit .env with your configuration
    ```

5. Add Firebase service account

   - Download serviceAccount.json from Firebase Console
   - Place it in the project root directory

## Running the Application

1. Start the Flask server

    ```bash
    python app.py
    ```

2. Access the application at `http://localhost:5000`

Note: To configure the application on Firebase, you'll need a secured `https` endpoint. So you can use any application like Tailscale as a reverse proxy.

3. Click on `Sign in with SSO` button. This should redirect you to Okta.
4. Log in to Okta using your credentials.
5. If verification is successful, you'll be redirected back to the application where you will see your name and email id along with a logout button.