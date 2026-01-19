from flask import Flask, redirect, url_for, session, render_template, request, flash
from authlib.integrations.flask_client import OAuth
from jwt import PyJWKClient
import os
import secrets, hashlib, base64, requests, jwt

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object('config')

# OAuth configuration
oauth = OAuth(app)
GOOGLE_ISSUER = "https://accounts.google.com"
DISCOVERY_URL = f"{GOOGLE_ISSUER}/.well-known/openid-configuration"

def get_google_cfg():
    return requests.get(DISCOVERY_URL).json()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dummy_login', methods=['POST'])
def dummy_login():
    username = request.form['username']
    password = request.form['password']
    # Dummy check for username and password
    if username == 'admin' and password == 'password':
        session['user'] = {'email': 'admin@example.com'}
        return redirect('/profile')
    else:
        flash('Invalid username or password')
        return redirect(url_for('index', error='Invalid username or password'))


@app.route('/login')
def login():
    cfg = get_google_cfg()
    authorization_endpoint = cfg["authorization_endpoint"]

    state = secrets.token_urlsafe(32)
    session["state"] = state

    code_verifier = secrets.token_urlsafe(64)
    session["code_verifier"] = code_verifier
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b"=").decode("utf-8")

    params = {
        "client_id": app.config["GOOGLE_CLIENT_ID"],
        "response_type": "code",
        "scope": "openid email profile",
        "redirect_uri": url_for("callback", _external=True),
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256"
    }

    auth_url = requests.Request("GET", authorization_endpoint, params=params).prepare().url
    return redirect(auth_url)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/callback')
def callback():
    if request.args.get("state") != session.get("state"):
        return "Invalid state", 400

    cfg = get_google_cfg()
    token_endpoint = cfg["token_endpoint"]
    jwks_uri = cfg["jwks_uri"]

    code = request.args.get("code")
    code_verifier = session.get("code_verifier")

    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": url_for("callback", _external=True),
        "client_id": app.config["GOOGLE_CLIENT_ID"],
        "client_secret": app.config["GOOGLE_CLIENT_SECRET"],
        "code_verifier": code_verifier
    }

    token_res = requests.post(token_endpoint, data=token_data).json()
    id_token = token_res.get("id_token")

    # Use PyJWKClient to fetch and verify the token with proper JWKS handling
    jwks_client = PyJWKClient(jwks_uri)
    signing_key = jwks_client.get_signing_key_from_jwt(id_token)
    
    claims = jwt.decode(
        id_token,
        signing_key.key,
        audience=app.config["GOOGLE_CLIENT_ID"],
        algorithms=["RS256"],
        options={"verify_aud": True, "verify_iss": True},
        issuer=GOOGLE_ISSUER
    )

    session["user"] = {
        "email": claims.get("email"),
        "name": claims.get("name"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "picture": claims.get("picture")
    }

    return redirect('/profile')


@app.route('/profile')
def profile():
    user = session.get('user')
    if user:
        return render_template('profile.html', user=user)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', False), host='0.0.0.0')
