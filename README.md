# Security Demo Application

A Flask-based web application that demonstrates various security features and data integrity concepts. This application serves as an educational tool to understand and test different security mechanisms.

## Features

- **Authentication & Authorization**
  - Secure login system
  - Role-based access control (Admin/User roles)
  - Session management
  - Authentication bypass simulation

- **Data Integrity**
  - File verification with SHA-256 hashing
  - Configuration management with digital signatures
  - TPM (Trusted Platform Module) simulation
  - Immutable logging system

- **Security Testing**
  - Authentication bypass simulation
  - Configuration tampering simulation
  - File integrity testing
  - Secure code execution (Admin only)

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Access the application:
   - Open your web browser
   - Navigate to `http://localhost:5000`

## Usage Guide

### Login Credentials

- **Admin Account**
  - Username: `admin`
  - Password: `SecurePassword123!`

- **Regular User Account**
  - Username: `user`
  - Password: `UserPassword456!`

### Available Features

#### For All Users
1. **File Verification**
   - Upload any file to verify its integrity
   - View SHA-256 hash of the file
   - Test file integrity checks

2. **System Status**
   - View current system status
   - Check TPM attestation status

#### Admin Only Features
1. **Configuration Management**
   - Toggle debug mode
   - Toggle maintenance mode
   - Test configuration tampering simulation

2. **Code Execution**
   - Execute Python code in a controlled environment
   - View execution results
   - Test secure code execution

### Security Testing

1. **Authentication Bypass Simulation**
   - Use the "Simulate Auth Bypass" button on the login page
   - Demonstrates what happens when authentication is bypassed

2. **Configuration Tampering**
   - Use the "Simulate Config Tampering" button in the dashboard
   - Shows the effects of unauthorized configuration changes

3. **File Integrity Testing**
   - Upload files to test integrity verification
   - View hash values and verification results

## Security Features

### 1. Immutable Logging
- All system activities are logged with cryptographic chaining
- Each log entry is linked to the previous one
- Prevents log tampering

### 2. TPM Simulation
- Simulates hardware-based security features
- Provides system integrity verification
- Demonstrates secure boot concepts

### 3. Digital Signatures
- Configuration changes are digitally signed
- Prevents unauthorized modifications
- Demonstrates code signing concepts

### 4. Secure Headers
- Content Security Policy (CSP)
- X-Content-Type-Options
- X-Frame-Options

## Project Structure

```
.
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── security/          # Security-related modules
│   ├── crypto.py      # Cryptographic functions
│   ├── middleware.py  # Security middleware
│   └── tpm.py         # TPM simulator
├── models/            # Data models
│   └── database.py    # Database simulation
├── utils/            # Utility functions
│   └── logging.py     # Logging setup
└── templates/        # HTML templates
    ├── index.html    # Homepage
    ├── login.html    # Login page
    └── dashboard.html # Dashboard
```

## Security Notes

1. This is a demonstration application and should not be used in production without proper security hardening
2. The TPM simulation is just that - a simulation. Real TPM hardware would be needed for production use
3. The code execution feature should be used with extreme caution
4. Default passwords should be changed in a production environment
5. The application includes intentionally vulnerable features for educational purposes

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 