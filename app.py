from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import hashlib
import hmac
import os
import json
import base64
import subprocess
import logging
from logging.handlers import RotatingFileHandler
from functools import wraps
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from utils.logging import setup_logger
from security.tpm import TPMSimulator
from security.crypto import generate_keys
from security.middleware import secure_headers, require_auth
from models.database import verify_user, update_config, configs

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Set up logging
logger = setup_logger()

# Initialize TPM simulator
tpm = TPMSimulator()
tpm.verify_boot_sequence()

# Generate keys for defense mechanisms
private_key, public_key = generate_keys()

# Apply security headers
app.after_request(secure_headers)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # ATTACK VECTOR 1: Authentication Bypass (related to data integrity)
        if 'bypass_auth' in request.form:
            session['user'] = username
            session['role'] = 'admin'  # Escalated privilege
            logger.warning(f"Authentication bypassed for user: {username}")
            return redirect(url_for('dashboard'))

        # DEFENSE: Proper password verification
        is_valid, role = verify_user(username, password)
        if is_valid:
            session['user'] = username
            session['role'] = role
            logger.info(f"User logged in: {username}")
            return redirect(url_for('dashboard'))

        error = "Invalid credentials"

    return render_template('login.html', error=error)

@app.route('/dashboard')
@require_auth
def dashboard():
    # TPM attestation for runtime integrity
    attestation_status, measurements = tpm.attestation()
    if not attestation_status:
        return "System integrity check failed", 500

    return render_template('dashboard.html',
                         username=session['user'],
                         role=session['role'],
                         configs=configs['app_settings'])

@app.route('/update_config', methods=['POST'])
@require_auth
def update_config_route():
    if session['role'] != 'admin':
        logger.warning(f"Unauthorized config update attempt by {session['user']}")
        return jsonify({"error": "Unauthorized"}), 403

    config_data = request.json

    # ATTACK VECTOR 2: Config Tampering (related to data integrity)
    if request.args.get('skip_verify') == '1':
        logger.warning(f"Config updated without verification: {config_data}")
        return jsonify({"status": "updated", "warning": "No verification performed"})

    try:
        update_config(config_data, private_key)
        logger.info(f"Config update by authorized user: {session['user']}")
        return jsonify({"status": "updated"})
    except Exception as e:
        logger.error(f"Config update failed: {str(e)}")
        return jsonify({"error": "Update failed"}), 500

@app.route('/verify_file', methods=['POST'])
@require_auth
def verify_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Simulate file integrity verification
    file_content = file.read()
    file_hash = hashlib.sha256(file_content).hexdigest()
    
    logger.info(f"File verification requested: {file.filename}")
    return jsonify({
        "filename": file.filename,
        "hash": file_hash,
        "status": "verified"
    })

@app.route('/execute_code', methods=['POST'])
@require_auth
def execute_code():
    if session['role'] != 'admin':
        return jsonify({"error": "Unauthorized"}), 403

    code = request.json.get('code')
    if not code:
        return jsonify({"error": "No code provided"}), 400

    try:
        # Simulate secure code execution
        result = subprocess.run(['python', '-c', code],
                              capture_output=True,
                              text=True,
                              timeout=5)
        return jsonify({
            "output": result.stdout,
            "error": result.stderr
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)