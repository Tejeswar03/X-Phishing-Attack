from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import requests
import logging


app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Mock user class
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Mock user database
users = {
    'test@example.com': User(1, 'test@example.com', 'password123'),
    'user@x.com': User(2, 'user@x.com', 'password456')
}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if str(user.id) == user_id:
            return user
    return None

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
        else:
            data = {
                'username': request.form.get('username'),
                'password': request.form.get('password')
            }

        username = data.get('username')
        password = data.get('password')
        
        # Log authentication attempt
        logger.info(f"Login attempt - Username: {username}")
        
        # Forward the request to the authentication server at port 5001
        try:
            response = requests.post('http://localhost:5001/login', json=data)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error connecting to authentication server: {e}")
            return jsonify({'success': False, 'message': 'Authentication server unavailable'}), 500

    return render_template('login.html')

@app.route('/password', methods=['GET'])
def password():
    username = request.args.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template('password.html', username=username)

@app.route('/auth/google')
def google_auth():
    logger.info("Google authentication initiated")
    # Implement Google authentication logic here
    return jsonify({'message': 'Google auth not implemented'})

@app.route('/auth/apple')
def apple_auth():
    logger.info("Apple authentication initiated")
    # Implement Apple authentication logic here
    return jsonify({'message': 'Apple auth not implemented'})

@app.route('/forgot-password')
def forgot_password():
    logger.info("Password reset requested")
    # Implement password reset logic here
    return jsonify({'message': 'Password reset not implemented'})


if __name__ == "__main__":
    from os import environ
    app.run(host="0.0.0.0", port=int(environ.get("PORT", 5000)))
    