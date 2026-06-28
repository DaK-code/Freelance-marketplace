from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app.auth import token_required, login_required
from app.utils import fetch_external_jobs, fetch_external_users, validate_email, format_response
import os
import requests

# Create blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)
auth_bp = Blueprint('auth', __name__)

# Fetch the Firebase Web API Key for REST authentication
FIREBASE_WEB_API_KEY = os.getenv('FIREBASE_API_KEY')

# MAIN ROUTES
@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/dashboard')
@login_required
def dashboard(): 
    return render_template('home.html', user=request.user)

# AUTH ROUTES
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not email or not validate_email(email):
            return render_template('signup.html', error='Invalid email format'), 400
        if not password or len(password) < 6:
            return render_template('signup.html', error='Password must be at least 6 characters long'), 400
        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match'), 400
        
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        
        response = requests.post(url, json=payload)
        result = response.json()
        
        if response.status_code == 200:
            session['user'] = {'email': result['email'], 'uid': result['localId']}
            session['token'] = result['idToken']
            
            return redirect(f"http://127.0.0.1:8000/?token={result['idToken']}")
        else:
            # Handle Firebase error 
            error_msg = result.get('error', {}).get('message', 'An error occurred during registration')
            return render_template('signup.html', error=error_msg), 400
            
    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return render_template('login.html', error='Email and password are required'), 400
        
        #  REAL CALL TO THE FIREBASE REST API FOR SIGNIN
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        
        response = requests.post(url, json=payload)
        result = response.json()
        
        if response.status_code == 200:
            session['user'] = {'email': result['email'], 'uid': result['localId']}
            session['token'] = result['idToken']
            
            #  MODIFIED: REDIRECT TO DJANGO HOMEPAGE WITH THE FIREBASE TOKEN
            return redirect(f"http://127.0.0.1:8000/?token={result['idToken']}")
        else:
            error_msg = result.get('error', {}).get('message', 'Incorrect email or password')
            return render_template('login.html', error=error_msg), 400
            
    return render_template('login.html')

@auth_bp.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect(url_for('main.home'))

@auth_bp.route('/reset', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form.get('email')
        
        if not email or not validate_email(email):
            return render_template('reset.html', error='Invalid email format'), 400
            
        #  REAL CALL TO THE FIREBASE REST API FOR PASSWORD RESET
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_WEB_API_KEY}"
        payload = {"requestType": "PASSWORD_RESET", "email": email}
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            return render_template('reset.html', message='A password reset link has been sent to your email address.'), 200
        else:
            result = response.json()
            error_msg = result.get('error', {}).get('message', 'An error occurred while processing your request')
            return render_template('reset.html', error=error_msg), 400
            
    return render_template('reset.html')




@api_bp.route('/login', methods=['POST'])
def api_login():
    """API endpoint for user login (Useful if Django queries Flask via JSON)"""
    data = request.get_json() or request.form
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return format_response({'error': 'Email and password are required'}, 400)
        
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    if response.status_code == 200:
        response_data = {
            'token': result['idToken'],
            'user': {'email': result['email'], 'uid': result['localId']}
        }
        return format_response(response_data, 200, 'Login successful')
    else:
        return format_response({'error': 'Invalid credentials'}, 400)




@api_bp.route('/services', methods=['GET'])
def get_services():
    services = [
        {"id": 1, "title": "Développement Web", "price": 500},
        {"id": 2, "title": "Design Logo", "price": 150}
    ]
    return jsonify(services)