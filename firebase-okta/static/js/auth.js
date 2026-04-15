import { 
    SAMLAuthProvider, 
    signInWithPopup,
    onAuthStateChanged 
} from 'https://www.gstatic.com/firebasejs/10.7.0/firebase-auth.js';
import { auth } from './firebase-config.js';

document.addEventListener('DOMContentLoaded', function() {
    // Create the SAML provider object
    const provider = new SAMLAuthProvider('saml.okta');
    
    // Add click handler to SSO button
    const ssoButton = document.getElementById('sso-button');
    if (ssoButton) {
        ssoButton.addEventListener('click', async () => {
            try {
                ssoButton.disabled = true;
                ssoButton.textContent = 'Signing in...';

                const result = await signInWithPopup(auth, provider);
                const idToken = await result.user.getIdToken();

                // Send token to backend
                const response = await fetch('/auth/verify-token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ idToken })
                });
                
                if (response.ok) {
                    window.location.reload();
                } else {
                    throw new Error('Failed to verify token with backend');
                }

            } catch (error) {
                console.error('Error during sign-in:', error);
                showError(error.message);
            } finally {
                ssoButton.disabled = false;
                ssoButton.textContent = 'Sign in with SSO';
            }
        });
    }

    function showError(message) {
        const errorDiv = document.getElementById('error-message');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
    }

    // Monitor auth state changes
    onAuthStateChanged(auth, (user) => {
        console.log('Auth state:', user ? 'logged in' : 'logged out');
    });
});