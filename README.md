# Cryptographic Operations GUI - Interactive Learning Tool

A PyQt6-based desktop application that provides an interactive interface for learning and experimenting with various cryptographic operations. This application serves as an educational tool to understand and practice different cryptographic concepts in a user-friendly environment.

## Features

- **Key Management**
  - Generate RSA key pairs
  - Export/Import keys
  - Key format verification
  - Secure key storage

- **Digital Signatures**
  - Create digital signatures
  - Verify signatures
  - Message authentication
  - Data integrity verification

- **HMAC Operations**
  - Generate HMAC (Hash-based Message Authentication Code)
  - Verify HMAC signatures
  - Data integrity checks
  - Key-based authentication

- **File Operations**
  - Sign files
  - Verify file signatures
  - File integrity checking
  - Secure file handling

- **Interactive Learning**
  - Step-by-step tutorials
  - Interactive demos
  - Operation history tracking
  - Real-time feedback

## Prerequisites

- Python 3.8 or higher
- PyQt6
- cryptography library

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

1. Start the application:
   ```bash
   python security/crypto_gui.py
   ```

2. The GUI will launch with the following tabs:
   - 🔑 Key Management
   - ✍️ Digital Signatures
   - 🔐 HMAC Operations
   - 📁 File Operations
   - 🎮 Demo Mode
   - 📜 History
   - 📚 Tutorials

## Usage Guide

### Key Management
1. Generate new key pairs
2. Export/Import keys
3. Verify key formats
4. Manage key storage

### Digital Signatures
1. Sign messages using private key
2. Verify signatures using public key
3. Test signature tampering
4. Practice message authentication

### HMAC Operations
1. Generate HMAC for data
2. Verify HMAC signatures
3. Test data integrity
4. Practice key-based authentication

### File Operations
1. Sign files
2. Verify file signatures
3. Check file integrity
4. Practice secure file handling

### Interactive Learning
1. Follow step-by-step tutorials
2. Try interactive demos
3. Track operation history
4. Learn through practice

## Project Structure

```
.
├── security/
│   ├── crypto_gui.py    # Main GUI application
│   └── crypto.py        # Cryptographic functions
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## Security Features

### 1. Key Management
- Secure key generation
- PEM format support
- Key validation
- Safe key storage

### 2. Digital Signatures
- RSA-based signatures
- Message authentication
- Data integrity verification
- Non-repudiation support

### 3. HMAC Operations
- SHA-256 based HMAC
- Key-based authentication
- Data integrity checks
- Tamper detection

### 4. File Security
- File signing
- Signature verification
- Integrity checking
- Secure file handling

## Educational Value

1. **Interactive Learning**
   - Hands-on experience with cryptographic operations
   - Real-time feedback on operations
   - Step-by-step tutorials
   - Visual demonstration of concepts

2. **Security Best Practices**
   - Proper key management
   - Secure signature verification
   - Data integrity protection
   - Safe file handling

3. **Practical Applications**
   - Message signing
   - File verification
   - Data integrity checks
   - Authentication practices

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 