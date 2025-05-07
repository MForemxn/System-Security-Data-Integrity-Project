import hashlib
import json
from security.crypto import sign_data

# Database simulation for demonstration purposes
users_db = {
    'admin': {
        'password': hashlib.sha256('SecurePassword123!'.encode()).hexdigest(),
        'role': 'admin'
    },
    'user': {
        'password': hashlib.sha256('UserPassword456!'.encode()).hexdigest(),
        'role': 'user'
    }
}

configs = {
    'app_settings': {
        'debug': False,
        'maintenance_mode': False,
        'allow_registration': True,
        'signature': ''  # To be signed with private key
    }
}

def sign_config(private_key):
    """Sign the configuration with the private key"""
    config_data = json.dumps(configs['app_settings'])
    configs['app_settings']['signature'] = sign_data(config_data, private_key)

def verify_user(username, password):
    """Verify user credentials"""
    if username in users_db:
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        if hashed_pw == users_db[username]['password']:
            return True, users_db[username]['role']
    return False, None

def update_config(config_data, private_key):
    """Update configuration and re-sign it"""
    configs['app_settings'].update(config_data)
    sign_config(private_key) 