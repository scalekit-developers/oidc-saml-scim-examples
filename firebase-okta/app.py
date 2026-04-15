from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-here')

# Initialize Firebase Admin SDK
cred = credentials.Certificate('serviceAccount.json') # Download serviceAccount.json from Firebase Console
firebase_admin.initialize_app(cred)

@app.route('/')
def index():
    user_data = None
    if 'user_id' in session:
        user_data = {
            'email': session.get('email'),
            'name': session.get('name')
        }
    return render_template('index.html', user=user_data)

@app.route('/auth/verify-token', methods=['POST'])
def verify_token():
    try:
        id_token = request.json.get('idToken')
        if not id_token:
            return jsonify({'error': 'No token provided'}), 400

        # Verify the token
        decoded_token = auth.verify_id_token(id_token)
        
        # Store user info in session
        session['user_id'] = decoded_token['uid']
        session['email'] = decoded_token.get('email', '')
        session['name'] = decoded_token.get('name', decoded_token.get('email', '').split('@')[0])

        return jsonify({'success': True}), 200

    except Exception as e:
        print(f"Token verification error: {e}")
        return jsonify({'error': str(e)}), 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)