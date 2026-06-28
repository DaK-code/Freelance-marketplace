import os
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from functools import wraps
from flask import request, jsonify, session

firebase_config = {
    'apiKey': os.getenv('FIREBASE_API_KEY'),
    'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
    'projectId': os.getenv('FIREBASE_PROJECT_ID'),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET'),
    'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    'appId': os.getenv('FIREBASE_APP_ID'),
}

try:
    if not firebase_admin._apps:  # Plus robuste que get_app() sans argument pour vérifier l'existence
        cred = credentials.Certificate('firebase-key.json') if os.path.exists('firebase-key.json') else None
        if cred:
            firebase_admin.initialize_app(cred)
except ValueError:
    pass

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Récupération propre du token dans le header Authorization
        auth_header = request.headers.get('Authorization', '')
        token = auth_header.replace('Bearer ', '') if auth_header.startswith('Bearer ') else None
        
        # Fallback sur la session si pas de token dans le header
        if not token and 'token' in session:
            token = session['token']
        
        # Rejet direct si aucun token n'est trouvé
        if not token:
            return jsonify({"message": "Unauthorized"}), 401
        
        try:
            # Validation stricte du token via Firebase
            decoded_token = firebase_auth.verify_id_token(token)
            request.user = decoded_token
        except Exception:
            # Rejet strict si le token est expiré ou invalide selon Firebase
            return jsonify({"message": "Unauthorized"}), 401
        
        return f(*args, **kwargs)
    return decorated

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return jsonify({"message": "Unauthorized"}), 401
        request.user = session['user']
        return f(*args, **kwargs)
    return decorated