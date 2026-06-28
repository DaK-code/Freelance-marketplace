import requests
import os
from flask import jsonify

EXTERNAL_API_URL = os.getenv('EXTERNAL_API_URL', 'https://jsonplaceholder.typicode.com')

def fetch_external_jobs():
    """Fetch jobs from external API (mock JSON Placeholder)"""
    try:
        response = requests.get(f'{EXTERNAL_API_URL}/posts', timeout=5)
        response.raise_for_status()
        posts = response.json()
        
        jobs = [
            {
                'id': post['id'],
                'title': f"Job #{post['id']}",
                'description': post['body'][:200],
                'client_id': post['userId'],
                'status': 'open'
            }
            for post in posts[:10]
        ]
        return jobs
    except requests.RequestException as e:
        return {'error': f'Failed to fetch jobs: {str(e)}'}

def fetch_external_users():
    """Fetch users from external API"""
    try:
        response = requests.get(f'{EXTERNAL_API_URL}/users', timeout=5)
        response.raise_for_status()
        users = response.json()
        
        return [
            {
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'company': user.get('company', {}).get('name', 'N/A')
            }
            for user in users[:5]
        ]
    except requests.RequestException as e:
        return {'error': f'Failed to fetch users: {str(e)}'}

def validate_email(email):
    """Basic email validation"""
    return '@' in email and '.' in email.split('@')[1]

def format_response(data, status_code=200, message=None):
    """Format API response"""
    response = {
        'status': 'success' if status_code < 400 else 'error',
        'data': data
    }
    if message:
        response['message'] = message
    return response, status_code
