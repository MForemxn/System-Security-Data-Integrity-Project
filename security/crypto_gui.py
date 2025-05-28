import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QTextEdit, QLabel, 
                            QFileDialog, QMessageBox, QTabWidget, QComboBox,
                            QProgressBar, QListWidget, QToolTip, QCheckBox,
                            QGroupBox, QRadioButton, QButtonGroup)
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QFont, QPalette, QColor
import base64
import os
from datetime import datetime
from crypto import (generate_keys, verify_hash_hmac, verify_signature, 
                   sign_data)
import hmac
import hashlib

# Theme styles
LIGHT_THEME = {
    'background': '#ffffff',
    'text': '#2c3e50',
    'button': '#3498db',
    'button_hover': '#2980b9',
    'success': '#2ecc71',
    'success_hover': '#27ae60',
    'danger': '#e74c3c',
    'danger_hover': '#c0392b',
    'border': '#bdc3c7',
    'hover': '#ecf0f1'
}

DARK_THEME = {
    'background': '#2c3e50',
    'text': '#ecf0f1',
    'button': '#3498db',
    'button_hover': '#2980b9',
    'success': '#2ecc71',
    'success_hover': '#27ae60',
    'danger': '#e74c3c',
    'danger_hover': '#c0392b',
    'border': '#34495e',
    'hover': '#34495e'
}

class InteractiveLabel(QLabel):
    def __init__(self, text, tooltip, parent=None):
        super().__init__(text, parent)
        self.setToolTip(tooltip)
        self.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                padding: 5px;
                border-radius: 3px;
            }
            QLabel:hover {
                background-color: #ecf0f1;
            }
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

class CryptoGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cryptographic Operations GUI - Interactive Learning Tool")
        self.setMinimumSize(1200, 800)
        
        # Initialize theme
        self.current_theme = LIGHT_THEME
        self.is_dark_mode = False
        
        # Initialize keys
        self.private_key = None
        self.public_key = None
        
        # Initialize operation history
        self.operation_history = []
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Add theme toggle button
        theme_btn = QPushButton("🌙 Toggle Dark Mode")
        theme_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.current_theme['button']};
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.current_theme['button_hover']};
            }}
        """)
        theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(theme_btn)
        
        # Add welcome message
        welcome_label = QLabel("Welcome to the Cryptographic Operations Learning Tool!")
        welcome_label.setStyleSheet(f"""
            QLabel {{
                color: {self.current_theme['text']};
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                background-color: {self.current_theme['hover']};
                border-radius: 5px;
            }}
        """)
        layout.addWidget(welcome_label)
        
        # Create tab widget
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {self.current_theme['border']};
                border-radius: 5px;
                background: {self.current_theme['background']};
            }}
            QTabBar::tab {{
                background: {self.current_theme['hover']};
                color: {self.current_theme['text']};
                padding: 8px 12px;
                margin: 2px;
                border-radius: 3px;
            }}
            QTabBar::tab:selected {{
                background: {self.current_theme['button']};
                color: white;
            }}
        """)
        layout.addWidget(tabs)
        
        # Create tabs for different operations
        self.create_key_management_tab(tabs)
        self.create_digital_signatures_tab(tabs)
        self.create_hmac_operations_tab(tabs)
        self.create_file_operations_tab(tabs)
        self.create_demo_tab(tabs)
        self.create_history_tab(tabs)
        self.create_tutorials_tab(tabs)
        
        # Add status bar
        self.statusBar().showMessage("Ready to explore cryptography!")
        
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.is_dark_mode = not self.is_dark_mode
        self.current_theme = DARK_THEME if self.is_dark_mode else LIGHT_THEME
        self.apply_theme()
        
    def apply_theme(self):
        """Apply the current theme to all widgets"""
        # Update main window background
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.current_theme['background']};
            }}
            QWidget {{
                background-color: {self.current_theme['background']};
                color: {self.current_theme['text']};
            }}
            QTextEdit {{
                background-color: {self.current_theme['background']};
                color: {self.current_theme['text']};
                border: 1px solid {self.current_theme['border']};
                border-radius: 5px;
            }}
            QPushButton {{
                background-color: {self.current_theme['button']};
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.current_theme['button_hover']};
            }}
            QGroupBox {{
                border: 1px solid {self.current_theme['border']};
                border-radius: 5px;
                margin-top: 1em;
                padding-top: 1em;
            }}
            QGroupBox::title {{
                color: {self.current_theme['text']};
            }}
        """)
        
        # Update theme toggle button text
        for widget in self.findChildren(QPushButton):
            if widget.text() in ["🌙 Toggle Dark Mode", "☀️ Toggle Light Mode"]:
                widget.setText("☀️ Toggle Light Mode" if self.is_dark_mode else "🌙 Toggle Dark Mode")
                break
        
    def add_to_history(self, operation_type, details):
        """Add an operation to the history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.operation_history.append({
            'timestamp': timestamp,
            'type': operation_type,
            'details': details
        })
        self.update_history_display()
        
    def update_history_display(self):
        """Update the history display widget"""
        self.history_list.clear()
        for entry in reversed(self.operation_history):
            self.history_list.addItem(
                f"[{entry['timestamp']}] {entry['type']}: {entry['details']}"
            )
        
    def create_key_management_tab(self, tabs):
        key_widget = QWidget()
        layout = QVBoxLayout(key_widget)
        
        # Add explanation
        explanation = InteractiveLabel(
            "🔑 Key Management",
            "Generate and manage your cryptographic key pairs. The private key stays with you, while the public key can be shared with others."
        )
        layout.addWidget(explanation)
        
        # Create split layout for generation and verification
        split_layout = QHBoxLayout()
        
        # Left side - Key Generation
        gen_group = QGroupBox("Key Generation")
        gen_layout = QVBoxLayout()
        
        generate_btn = QPushButton("Generate New Key Pair")
        generate_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.current_theme['button']};
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.current_theme['button_hover']};
            }}
        """)
        generate_btn.clicked.connect(self.generate_new_keys)
        gen_layout.addWidget(generate_btn)
        
        # Add export/import buttons
        key_management_layout = QHBoxLayout()
        
        export_btn = QPushButton("Export Keys")
        export_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.current_theme['success']};
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.current_theme['success_hover']};
            }}
        """)
        export_btn.clicked.connect(self.export_keys)
        key_management_layout.addWidget(export_btn)
        
        import_btn = QPushButton("Import Keys")
        import_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.current_theme['button']};
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.current_theme['button_hover']};
            }}
        """)
        import_btn.clicked.connect(self.import_keys)
        key_management_layout.addWidget(import_btn)
        
        gen_layout.addLayout(key_management_layout)
        
        self.private_key_display = QTextEdit()
        self.private_key_display.setReadOnly(True)
        self.private_key_display.setPlaceholderText("Your private key will appear here - keep it secret!")
        gen_layout.addWidget(InteractiveLabel("Private Key:", "This is your secret key - never share it!"))
        gen_layout.addWidget(self.private_key_display)
        
        self.public_key_display = QTextEdit()
        self.public_key_display.setReadOnly(True)
        self.public_key_display.setPlaceholderText("Your public key will appear here - you can share this!")
        gen_layout.addWidget(InteractiveLabel("Public Key:", "This is your public key - safe to share with others!"))
        gen_layout.addWidget(self.public_key_display)
        
        gen_group.setLayout(gen_layout)
        split_layout.addWidget(gen_group)
        
        # Right side - Key Verification
        verify_group = QGroupBox("Key Verification")
        verify_layout = QVBoxLayout()
        
        self.verify_key_input = QTextEdit()
        self.verify_key_input.setPlaceholderText("Enter a public key to verify...")
        verify_layout.addWidget(InteractiveLabel("Public Key to Verify:", "Enter a public key to verify its format and validity"))
        verify_layout.addWidget(self.verify_key_input)
        
        verify_key_btn = QPushButton("Verify Key")
        verify_key_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.current_theme['success']};
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.current_theme['success_hover']};
            }}
        """)
        verify_key_btn.clicked.connect(self.verify_key_action)
        verify_layout.addWidget(verify_key_btn)
        
        self.key_verify_result = QLabel("")
        self.key_verify_result.setStyleSheet(f"""
            QLabel {{
                background-color: {self.current_theme['background']};
                padding: 10px;
                border-radius: 5px;
                border: 1px solid {self.current_theme['border']};
                font-weight: bold;
            }}
        """)
        verify_layout.addWidget(self.key_verify_result)
        
        verify_group.setLayout(verify_layout)
        split_layout.addWidget(verify_group)
        
        layout.addLayout(split_layout)
        tabs.addTab(key_widget, "🔑 Key Management")
        
    def create_digital_signatures_tab(self, tabs):
        sign_widget = QWidget()
        layout = QVBoxLayout(sign_widget)
        
        # Add explanation
        explanation = InteractiveLabel(
            "✍️ Digital Signatures",
            "Create and verify digital signatures using your key pair. Signatures prove message authenticity and integrity."
        )
        layout.addWidget(explanation)
        
        # Create split layout for signing and verification
        split_layout = QHBoxLayout()
        
        # Left side - Signing
        sign_group = QGroupBox("Create Signature")
        sign_layout = QVBoxLayout()
        
        self.sign_input = QTextEdit()
        self.sign_input.setPlaceholderText("Enter the message you want to sign...")
        sign_layout.addWidget(InteractiveLabel("Message to Sign:", "Enter the message you want to sign with your private key"))
        sign_layout.addWidget(self.sign_input)
        
        sign_btn = QPushButton("Sign Message")
        sign_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        sign_btn.clicked.connect(self.sign_data_action)
        sign_layout.addWidget(sign_btn)
        
        self.signature_display = QTextEdit()
        self.signature_display.setReadOnly(True)
        self.signature_display.setPlaceholderText("Your signature will appear here...")
        sign_layout.addWidget(InteractiveLabel("Generated Signature:", "The signature generated for your message"))
        sign_layout.addWidget(self.signature_display)
        
        sign_group.setLayout(sign_layout)
        split_layout.addWidget(sign_group)
        
        # Right side - Verification
        verify_group = QGroupBox("Verify Signature")
        verify_layout = QVBoxLayout()
        
        self.verify_data_input = QTextEdit()
        self.verify_data_input.setPlaceholderText("Enter the message to verify...")
        verify_layout.addWidget(InteractiveLabel("Message:", "Enter the message that was signed"))
        verify_layout.addWidget(self.verify_data_input)
        
        self.verify_signature_input = QTextEdit()
        self.verify_signature_input.setPlaceholderText("Enter the signature to verify...")
        verify_layout.addWidget(InteractiveLabel("Signature:", "Enter the signature to verify"))
        verify_layout.addWidget(self.verify_signature_input)
        
        verify_btn = QPushButton("Verify Signature")
        verify_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        verify_btn.clicked.connect(self.verify_signature_action)
        verify_layout.addWidget(verify_btn)
        
        self.verify_result = QLabel("")
        self.verify_result.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #dee2e6;
                font-weight: bold;
            }
        """)
        verify_layout.addWidget(self.verify_result)
        
        verify_group.setLayout(verify_layout)
        split_layout.addWidget(verify_group)
        
        layout.addLayout(split_layout)
        tabs.addTab(sign_widget, "✍️ Digital Signatures")
        
    def create_hmac_operations_tab(self, tabs):
        hmac_widget = QWidget()
        layout = QVBoxLayout(hmac_widget)
        
        # Add explanation
        explanation = InteractiveLabel(
            "🔐 HMAC Operations",
            "Create and verify HMAC (Hash-based Message Authentication Code) for data integrity verification."
        )
        layout.addWidget(explanation)
        
        # Create split layout for generation and verification
        split_layout = QHBoxLayout()
        
        # Left side - HMAC Generation
        gen_group = QGroupBox("Generate HMAC")
        gen_layout = QVBoxLayout()
        
        self.hmac_gen_data_input = QTextEdit()
        self.hmac_gen_data_input.setPlaceholderText("Enter the data to generate HMAC for...")
        gen_layout.addWidget(InteractiveLabel("Data:", "Enter the data you want to generate an HMAC for"))
        gen_layout.addWidget(self.hmac_gen_data_input)
        
        self.hmac_gen_key_input = QTextEdit()
        self.hmac_gen_key_input.setPlaceholderText("Enter the HMAC key...")
        gen_layout.addWidget(InteractiveLabel("Key:", "Enter the key to use for HMAC generation"))
        gen_layout.addWidget(self.hmac_gen_key_input)
        
        generate_hmac_btn = QPushButton("Generate HMAC")
        generate_hmac_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        generate_hmac_btn.clicked.connect(self.generate_hmac_action)
        gen_layout.addWidget(generate_hmac_btn)
        
        self.hmac_gen_output = QTextEdit()
        self.hmac_gen_output.setReadOnly(True)
        self.hmac_gen_output.setPlaceholderText("Generated HMAC will appear here...")
        gen_layout.addWidget(InteractiveLabel("Generated HMAC:", "The HMAC generated for your data"))
        gen_layout.addWidget(self.hmac_gen_output)
        
        gen_group.setLayout(gen_layout)
        split_layout.addWidget(gen_group)
        
        # Right side - HMAC Verification
        verify_group = QGroupBox("Verify HMAC")
        verify_layout = QVBoxLayout()
        
        self.hmac_data_input = QTextEdit()
        self.hmac_data_input.setPlaceholderText("Enter the data to verify...")
        verify_layout.addWidget(InteractiveLabel("Data:", "Enter the data to verify"))
        verify_layout.addWidget(self.hmac_data_input)
        
        self.hmac_key_input = QTextEdit()
        self.hmac_key_input.setPlaceholderText("Enter the HMAC key...")
        verify_layout.addWidget(InteractiveLabel("Key:", "Enter the key used for HMAC generation"))
        verify_layout.addWidget(self.hmac_key_input)
        
        self.hmac_signature_input = QTextEdit()
        self.hmac_signature_input.setPlaceholderText("Enter the HMAC to verify...")
        verify_layout.addWidget(InteractiveLabel("HMAC:", "Enter the HMAC to verify"))
        verify_layout.addWidget(self.hmac_signature_input)
        
        verify_hmac_btn = QPushButton("Verify HMAC")
        verify_hmac_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        verify_hmac_btn.clicked.connect(self.verify_hmac_action)
        verify_layout.addWidget(verify_hmac_btn)
        
        self.hmac_result = QLabel("")
        self.hmac_result.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #dee2e6;
                font-weight: bold;
            }
        """)
        verify_layout.addWidget(self.hmac_result)
        
        verify_group.setLayout(verify_layout)
        split_layout.addWidget(verify_group)
        
        layout.addLayout(split_layout)
        tabs.addTab(hmac_widget, "🔐 HMAC Operations")
        
    def create_file_operations_tab(self, tabs):
        file_widget = QWidget()
        layout = QVBoxLayout(file_widget)
        
        # Add explanation
        explanation = InteractiveLabel(
            "📁 File Operations",
            "Sign and verify files to ensure their integrity and authenticity."
        )
        layout.addWidget(explanation)
        
        # Create split layout for signing and verification
        split_layout = QHBoxLayout()
        
        # Left side - File Signing
        sign_group = QGroupBox("Sign File")
        sign_layout = QVBoxLayout()
        
        file_select_btn = QPushButton("Select File")
        file_select_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        file_select_btn.clicked.connect(self.select_file_to_sign)
        sign_layout.addWidget(file_select_btn)
        
        self.file_path_display = QLabel("No file selected")
        self.file_path_display.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #dee2e6;
            }
        """)
        sign_layout.addWidget(self.file_path_display)
        
        sign_file_btn = QPushButton("Sign File")
        sign_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        sign_file_btn.clicked.connect(self.sign_file_action)
        sign_layout.addWidget(sign_file_btn)
        
        self.file_signature_display = QTextEdit()
        self.file_signature_display.setReadOnly(True)
        self.file_signature_display.setPlaceholderText("File signature will appear here...")
        sign_layout.addWidget(InteractiveLabel("File Signature:", "The signature generated for your file"))
        sign_layout.addWidget(self.file_signature_display)
        
        sign_group.setLayout(sign_layout)
        split_layout.addWidget(sign_group)
        
        # Right side - File Verification
        verify_group = QGroupBox("Verify File")
        verify_layout = QVBoxLayout()
        
        verify_file_select_btn = QPushButton("Select File")
        verify_file_select_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        verify_file_select_btn.clicked.connect(self.select_file_to_verify)
        verify_layout.addWidget(verify_file_select_btn)
        
        self.verify_file_path_display = QLabel("No file selected")
        self.verify_file_path_display.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #dee2e6;
            }
        """)
        verify_layout.addWidget(self.verify_file_path_display)
        
        self.verify_file_signature_input = QTextEdit()
        self.verify_file_signature_input.setPlaceholderText("Enter the file signature to verify...")
        verify_layout.addWidget(InteractiveLabel("File Signature:", "Enter the signature to verify"))
        verify_layout.addWidget(self.verify_file_signature_input)
        
        verify_file_btn = QPushButton("Verify File")
        verify_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        verify_file_btn.clicked.connect(self.verify_file_action)
        verify_layout.addWidget(verify_file_btn)
        
        self.file_verify_result = QLabel("")
        self.file_verify_result.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #dee2e6;
                font-weight: bold;
            }
        """)
        verify_layout.addWidget(self.file_verify_result)
        
        verify_group.setLayout(verify_layout)
        split_layout.addWidget(verify_group)
        
        layout.addLayout(split_layout)
        tabs.addTab(file_widget, "📁 File Operations")
        
    def create_demo_tab(self, tabs):
        demo_widget = QWidget()
        layout = QVBoxLayout(demo_widget)
        
        # Add interactive demo header
        demo_header = InteractiveLabel(
            "🎮 Interactive Demo Mode",
            "Try out different cryptographic operations with pre-configured examples. Feel free to modify the inputs and see what happens!"
        )
        layout.addWidget(demo_header)
        
        # Demo scenarios dropdown with better styling
        scenario_group = QGroupBox("Choose Your Demo")
        scenario_layout = QVBoxLayout()
        
        self.demo_scenarios = QComboBox()
        self.demo_scenarios.addItems([
            "Sign a Message",
            "Verify a Signature",
            "HMAC Verification",
            "File Integrity Check"
        ])
        self.demo_scenarios.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                background: white;
            }
            QComboBox:hover {
                border-color: #3498db;
            }
        """)
        self.demo_scenarios.currentIndexChanged.connect(self.update_demo_description)
        scenario_layout.addWidget(self.demo_scenarios)
        scenario_group.setLayout(scenario_layout)
        layout.addWidget(scenario_group)
        
        # Demo description with better formatting
        self.demo_description = QLabel("")
        self.demo_description.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #dee2e6;
            }
        """)
        layout.addWidget(self.demo_description)
        
        # Interactive input area
        input_group = QGroupBox("Your Input")
        input_layout = QVBoxLayout()
        
        self.demo_input = QTextEdit()
        self.demo_input.setPlaceholderText("Modify the input here to see how it affects the cryptographic operations!")
        input_layout.addWidget(self.demo_input)
        
        # Add customization options
        options_layout = QHBoxLayout()
        self.auto_generate_keys = QCheckBox("Auto-generate keys if needed")
        self.auto_generate_keys.setChecked(True)
        options_layout.addWidget(self.auto_generate_keys)
        
        self.show_details = QCheckBox("Show detailed process")
        self.show_details.setChecked(True)
        options_layout.addWidget(self.show_details)
        
        input_layout.addLayout(options_layout)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Demo output area with better formatting
        output_group = QGroupBox("Results")
        output_layout = QVBoxLayout()
        
        self.demo_output = QTextEdit()
        self.demo_output.setReadOnly(True)
        self.demo_output.setPlaceholderText("Results will appear here...")
        output_layout.addWidget(self.demo_output)
        
        # Progress bar with better styling
        self.demo_progress = QProgressBar()
        self.demo_progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bdc3c7;
                border-radius: 3px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
            }
        """)
        output_layout.addWidget(self.demo_progress)
        
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        # Demo buttons with better styling
        button_layout = QHBoxLayout()
        
        run_demo_btn = QPushButton("Run Demo")
        run_demo_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 8px 15px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        run_demo_btn.clicked.connect(self.run_demo)
        button_layout.addWidget(run_demo_btn)
        
        clear_demo_btn = QPushButton("Clear")
        clear_demo_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 15px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        clear_demo_btn.clicked.connect(self.clear_demo)
        button_layout.addWidget(clear_demo_btn)
        
        layout.addLayout(button_layout)
        
        tabs.addTab(demo_widget, "🎮 Demo Mode")
        
    def create_history_tab(self, tabs):
        history_widget = QWidget()
        layout = QVBoxLayout(history_widget)
        
        # Add explanation
        explanation = InteractiveLabel(
            "📜 Operation History",
            "This shows a history of all cryptographic operations you've performed. Use this to track your learning progress!"
        )
        layout.addWidget(explanation)
        
        # History list
        history_group = QGroupBox("Operation History")
        history_layout = QVBoxLayout()
        
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 3px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #dee2e6;
            }
            QListWidget::item:hover {
                background-color: #ecf0f1;
            }
        """)
        history_layout.addWidget(self.history_list)
        history_group.setLayout(history_layout)
        layout.addWidget(history_group)
        
        # Clear history button
        clear_history_btn = QPushButton("Clear History")
        clear_history_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        clear_history_btn.clicked.connect(self.clear_history)
        layout.addWidget(clear_history_btn)
        
        tabs.addTab(history_widget, "📜 History")
        
    def create_tutorials_tab(self, tabs):
        """Create the tutorials tab with interactive learning content"""
        tutorial_widget = QWidget()
        layout = QVBoxLayout(tutorial_widget)
        
        # Add explanation
        explanation = InteractiveLabel(
            "📚 Interactive Tutorials",
            "Learn about cryptography through interactive tutorials and examples."
        )
        layout.addWidget(explanation)
        
        # Tutorial selection
        tutorial_group = QGroupBox("Choose a Tutorial")
        tutorial_layout = QVBoxLayout()
        
        self.tutorial_list = QComboBox()
        self.tutorial_list.addItems([
            "Introduction to Cryptography",
            "Understanding Key Pairs",
            "Digital Signatures Explained",
            "HMAC and Data Integrity",
            "Security Best Practices"
        ])
        self.tutorial_list.setStyleSheet(f"""
            QComboBox {{
                padding: 5px;
                border: 1px solid {self.current_theme['border']};
                border-radius: 3px;
                background: {self.current_theme['background']};
                color: {self.current_theme['text']};
            }}
            QComboBox:hover {{
                border-color: {self.current_theme['button']};
            }}
        """)
        self.tutorial_list.currentIndexChanged.connect(self.update_tutorial_content)
        tutorial_layout.addWidget(self.tutorial_list)
        tutorial_group.setLayout(tutorial_layout)
        layout.addWidget(tutorial_group)
        
        # Tutorial content
        content_group = QGroupBox("Tutorial Content")
        content_layout = QVBoxLayout()
        
        self.tutorial_content = QTextEdit()
        self.tutorial_content.setReadOnly(True)
        self.tutorial_content.setStyleSheet(f"""
            QTextEdit {{
                background-color: {self.current_theme['background']};
                color: {self.current_theme['text']};
                border: 1px solid {self.current_theme['border']};
                border-radius: 5px;
                padding: 10px;
            }}
        """)
        content_layout.addWidget(self.tutorial_content)
        
        # Interactive example section
        example_group = QGroupBox("Try It Yourself")
        example_layout = QVBoxLayout()
        
        self.tutorial_example = QTextEdit()
        self.tutorial_example.setPlaceholderText("Try the example here...")
        example_layout.addWidget(self.tutorial_example)
        
        run_example_btn = QPushButton("Run Example")
        run_example_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.current_theme['button']};
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.current_theme['button_hover']};
            }}
        """)
        run_example_btn.clicked.connect(self.run_tutorial_example)
        example_layout.addWidget(run_example_btn)
        
        self.example_output = QTextEdit()
        self.example_output.setReadOnly(True)
        self.example_output.setPlaceholderText("Example output will appear here...")
        example_layout.addWidget(self.example_output)
        
        example_group.setLayout(example_layout)
        content_layout.addWidget(example_group)
        
        content_group.setLayout(content_layout)
        layout.addWidget(content_group)
        
        tabs.addTab(tutorial_widget, "📚 Tutorials")
        
    def update_tutorial_content(self):
        """Update the tutorial content based on selection"""
        tutorial = self.tutorial_list.currentText()
        content = {
            "Introduction to Cryptography": """
                <h2>Introduction to Cryptography</h2>
                <p>Cryptography is the practice of securing information through mathematical techniques.</p>
                <h3>Key Concepts:</h3>
                <ul>
                    <li>Confidentiality: Keeping information secret</li>
                    <li>Integrity: Ensuring information hasn't been altered</li>
                    <li>Authentication: Verifying the source of information</li>
                </ul>
                <h3>Try it yourself:</h3>
                <p>Enter a message below to see how it can be secured using different cryptographic techniques.</p>
            """,
            "Understanding Key Pairs": """
                <h2>Understanding Key Pairs</h2>
                <p>Public key cryptography uses a pair of keys:</p>
                <ul>
                    <li>Public Key: Can be shared with anyone</li>
                    <li>Private Key: Must be kept secret</li>
                </ul>
                <h3>Try it yourself:</h3>
                <p>Generate a key pair and see how they work together.</p>
            """,
            "Digital Signatures Explained": """
                <h2>Digital Signatures</h2>
                <p>Digital signatures provide:</p>
                <ul>
                    <li>Authentication: Proves who created the message</li>
                    <li>Integrity: Ensures the message hasn't been altered</li>
                    <li>Non-repudiation: Sender cannot deny sending the message</li>
                </ul>
                <h3>Try it yourself:</h3>
                <p>Sign a message and verify its authenticity.</p>
            """,
            "HMAC and Data Integrity": """
                <h2>HMAC (Hash-based Message Authentication Code)</h2>
                <p>HMAC provides:</p>
                <ul>
                    <li>Message authentication</li>
                    <li>Data integrity verification</li>
                    <li>Protection against tampering</li>
                </ul>
                <h3>Try it yourself:</h3>
                <p>Generate an HMAC for a message and verify its integrity.</p>
            """,
            "Security Best Practices": """
                <h2>Security Best Practices</h2>
                <p>Important security guidelines:</p>
                <ul>
                    <li>Never share your private key</li>
                    <li>Use strong, unique keys</li>
                    <li>Regularly rotate keys</li>
                    <li>Verify signatures before trusting data</li>
                    <li>Keep software updated</li>
                </ul>
                <h3>Try it yourself:</h3>
                <p>Practice secure key management and verification.</p>
            """
        }
        self.tutorial_content.setHtml(content.get(tutorial, "Select a tutorial to begin."))
        
    def run_tutorial_example(self):
        """Run the selected tutorial example"""
        tutorial = self.tutorial_list.currentText()
        example_input = self.tutorial_example.toPlainText()
        
        try:
            if tutorial == "Introduction to Cryptography":
                # Simple encryption example
                if example_input:
                    encoded = base64.b64encode(example_input.encode()).decode()
                    self.example_output.setText(f"Encoded message: {encoded}")
                else:
                    self.example_output.setText("Please enter a message to encode.")
                    
            elif tutorial == "Understanding Key Pairs":
                if not self.private_key:
                    self.generate_new_keys()
                self.example_output.setText(
                    f"Generated Key Pair:\n\n"
                    f"Public Key:\n{self.public_key}\n\n"
                    f"Private Key:\n{self.private_key}"
                )
                
            elif tutorial == "Digital Signatures Explained":
                if not self.private_key:
                    self.generate_new_keys()
                if example_input:
                    signature = sign_data(example_input, self.private_key)
                    self.example_output.setText(
                        f"Message: {example_input}\n\n"
                        f"Signature: {signature}\n\n"
                        f"Try verifying this signature in the Digital Signatures tab!"
                    )
                else:
                    self.example_output.setText("Please enter a message to sign.")
                    
            elif tutorial == "HMAC and Data Integrity":
                if example_input:
                    key = "tutorial_key"
                    signature = hmac.new(key.encode(), example_input.encode(), hashlib.sha256).hexdigest()
                    self.example_output.setText(
                        f"Message: {example_input}\n\n"
                        f"HMAC: {signature}\n\n"
                        f"Try verifying this HMAC in the HMAC Operations tab!"
                    )
                else:
                    self.example_output.setText("Please enter a message to generate HMAC for.")
                    
            elif tutorial == "Security Best Practices":
                self.example_output.setText(
                    "Security Checklist:\n\n"
                    "✓ Generate new keys\n"
                    "✓ Sign a message\n"
                    "✓ Verify a signature\n"
                    "✓ Generate an HMAC\n"
                    "✓ Verify file integrity\n\n"
                    "Complete these tasks to practice secure operations!"
                )
                
        except Exception as e:
            self.example_output.setText(f"Error: {str(e)}")
            
    def export_keys(self):
        """Export keys to files"""
        if not self.private_key or not self.public_key:
            QMessageBox.warning(self, "Warning", "Please generate keys first!")
            return
            
        try:
            # Export private key
            private_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Private Key",
                "",
                "PEM Files (*.pem);;All Files (*.*)"
            )
            if private_path:
                with open(private_path, "w") as f:
                    f.write(str(self.private_key))
                    
            # Export public key
            public_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Public Key",
                "",
                "PEM Files (*.pem);;All Files (*.*)"
            )
            if public_path:
                with open(public_path, "w") as f:
                    f.write(str(self.public_key))
                    
            QMessageBox.information(self, "Success", "Keys exported successfully!")
            self.add_to_history("Export", "Exported key pair")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export keys: {str(e)}")
            
    def import_keys(self):
        """Import keys from files"""
        try:
            # Import private key
            private_path, _ = QFileDialog.getOpenFileName(
                self,
                "Open Private Key",
                "",
                "PEM Files (*.pem);;All Files (*.*)"
            )
            if private_path:
                with open(private_path, "r") as f:
                    self.private_key = f.read()
                    self.private_key_display.setText(self.private_key)
                    
            # Import public key
            public_path, _ = QFileDialog.getOpenFileName(
                self,
                "Open Public Key",
                "",
                "PEM Files (*.pem);;All Files (*.*)"
            )
            if public_path:
                with open(public_path, "r") as f:
                    self.public_key = f.read()
                    self.public_key_display.setText(self.public_key)
                    
            QMessageBox.information(self, "Success", "Keys imported successfully!")
            self.add_to_history("Import", "Imported key pair")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to import keys: {str(e)}")

    def update_demo_description(self):
        """Update the demo description based on the selected scenario"""
        scenario = self.demo_scenarios.currentText()
        descriptions = {
            "Sign a Message": """
                <b>Sign a Message Demo</b><br>
                This demo shows how to sign a message using your private key.<br>
                Try modifying the message to see how the signature changes!<br>
                <i>Tip: The signature will be different for each unique message.</i>
            """,
            "Verify a Signature": """
                <b>Verify a Signature Demo</b><br>
                This demo shows how to verify a signature using the public key.<br>
                Try changing the message or signature to see how verification works!<br>
                <i>Tip: Even a small change in the message will make the verification fail.</i>
            """,
            "HMAC Verification": """
                <b>HMAC Verification Demo</b><br>
                This demo shows how to verify data integrity using HMAC.<br>
                Try changing the message, key, or signature to see the effects!<br>
                <i>Tip: HMAC ensures both authenticity and integrity of the message.</i>
            """,
            "File Integrity Check": """
                <b>File Integrity Check Demo</b><br>
                This demo shows how to verify file integrity using HMAC.<br>
                A temporary file will be created for demonstration.<br>
                <i>Tip: This is how software updates verify their integrity!</i>
            """
        }
        self.demo_description.setText(descriptions.get(scenario, ""))
        
    def run_demo(self):
        """Run the selected demo scenario with enhanced interactivity"""
        scenario = self.demo_scenarios.currentText()
        self.demo_progress.setValue(0)
        
        # Show step-by-step process if enabled
        def show_step(step, value):
            if self.show_details.isChecked():
                self.demo_output.append(f"Step {step}: {value}")
            self.demo_progress.setValue(25 * step)
        
        try:
            if scenario == "Sign a Message":
                show_step(1, "Preparing to sign message...")
                if not self.private_key and self.auto_generate_keys.isChecked():
                    show_step(2, "Generating new key pair...")
                    self.generate_new_keys()
                
                data = self.demo_input.toPlainText() or "Hello, this is a demo message!"
                show_step(3, f"Signing message: {data[:30]}...")
                signature = sign_data(data, self.private_key)
                
                show_step(4, "Signature generated successfully!")
                self.demo_output.setText(
                    f"Message: {data}\n\n"
                    f"Signature: {signature}\n\n"
                    f"Try changing the message and signing again to see how the signature changes!"
                )
                self.add_to_history("Demo Sign", f"Signed message: {data[:20]}...")
                
            elif scenario == "Verify a Signature":
                show_step(1, "Preparing to verify signature...")
                if not self.public_key and self.auto_generate_keys.isChecked():
                    show_step(2, "Generating new key pair...")
                    self.generate_new_keys()
                
                data = self.demo_input.toPlainText()
                signature = sign_data(data, self.private_key)
                show_step(3, f"Verifying signature for message: {data[:30]}...")
                
                is_valid = verify_signature(data, base64.b64decode(signature), self.public_key)
                show_step(4, "Verification complete!")
                
                self.demo_output.setText(
                    f"Message: {data}\n\n"
                    f"Signature: {signature}\n\n"
                    f"Verification: {'✅ Successful' if is_valid else '❌ Failed'}\n\n"
                    f"Try modifying the message or signature to see how verification works!"
                )
                self.add_to_history("Demo Verify", f"Verified message: {data[:20]}...")
                
            elif scenario == "HMAC Verification":
                show_step(1, "Preparing HMAC verification...")
                data = self.demo_input.toPlainText()
                key = "demo_secret_key"
                signature = hmac.new(key.encode(), data.encode(), hashlib.sha256).hexdigest()
                
                show_step(2, f"Generated HMAC for message: {data[:30]}...")
                show_step(3, "Verifying HMAC...")
                
                is_valid = verify_hash_hmac(data, signature, key.encode())
                show_step(4, "Verification complete!")
                
                self.demo_output.setText(
                    f"Message: {data}\n\n"
                    f"Key: {key}\n\n"
                    f"HMAC: {signature}\n\n"
                    f"Verification: {'✅ Successful' if is_valid else '❌ Failed'}\n\n"
                    f"Try changing the message, key, or HMAC to see how verification works!"
                )
                self.add_to_history("Demo HMAC", f"Verified HMAC for: {data[:20]}...")
                
            elif scenario == "File Integrity Check":
                show_step(1, "Creating demo file...")
                demo_file = "demo_message.txt"
                with open(demo_file, "w") as f:
                    f.write("This is a demo file for integrity checking.")
                
                show_step(2, f"Reading file: {demo_file}...")
                with open(demo_file, "rb") as f:
                    data = f.read().decode()
                
                key = "demo_file_key"
                show_step(3, "Generating HMAC for file...")
                signature = hmac.new(key.encode(), data.encode(), hashlib.sha256).hexdigest()
                
                show_step(4, "Verifying file integrity...")
                is_valid = verify_hash_hmac(data, signature, key.encode())
                
                self.demo_output.setText(
                    f"File: {demo_file}\n\n"
                    f"Content: {data}\n\n"
                    f"HMAC: {signature}\n\n"
                    f"Verification: {'✅ Successful' if is_valid else '❌ Failed'}\n\n"
                    f"This is how software updates verify their integrity!"
                )
                self.add_to_history("Demo File Check", f"Verified file: {demo_file}")
                os.remove(demo_file)  # Clean up
            
            self.demo_progress.setValue(100)
            
        except Exception as e:
            self.demo_output.setText(f"❌ Error: {str(e)}\n\nTry again or check your input!")
            self.demo_progress.setValue(0)
        
    def clear_demo(self):
        """Clear the demo input and output"""
        self.demo_input.clear()
        self.demo_output.clear()
        self.demo_progress.setValue(0)
        
    def clear_history(self):
        """Clear the operation history"""
        self.operation_history.clear()
        self.history_list.clear()
        
    def generate_new_keys(self):
        try:
            self.private_key, self.public_key = generate_keys()
            self.private_key_display.setText(str(self.private_key))
            self.public_key_display.setText(str(self.public_key))
            self.add_to_history("Key Generation", "Generated new key pair")
            QMessageBox.information(self, "Success", "New key pair generated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate keys: {str(e)}")
            
    def sign_data_action(self):
        if not self.private_key:
            QMessageBox.warning(self, "Warning", "Please generate keys first!")
            return
            
        try:
            data = self.sign_input.toPlainText()
            if not data:
                QMessageBox.warning(self, "Warning", "Please enter data to sign!")
                return
                
            signature = sign_data(data, self.private_key)
            self.signature_display.setText(signature)
            self.add_to_history("Sign", f"Signed data: {data[:20]}...")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to sign data: {str(e)}")
            
    def verify_signature_action(self):
        if not self.public_key:
            QMessageBox.warning(self, "Warning", "Please generate keys first!")
            return
            
        try:
            data = self.verify_data_input.toPlainText()
            signature = self.verify_signature_input.toPlainText()
            
            if not data or not signature:
                QMessageBox.warning(self, "Warning", "Please enter both data and signature!")
                return
                
            # Convert signature from base64
            signature_bytes = base64.b64decode(signature)
            
            is_valid = verify_signature(data, signature_bytes, self.public_key)
            self.verify_result.setText(f"Verification {'Successful' if is_valid else 'Failed'}")
            self.verify_result.setStyleSheet(
                "color: green;" if is_valid else "color: red;"
            )
            self.add_to_history("Verify", f"Verified data: {data[:20]}...")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to verify signature: {str(e)}")
            
    def verify_hmac_action(self):
        try:
            data = self.hmac_data_input.toPlainText()
            key = self.hmac_key_input.toPlainText()
            signature = self.hmac_signature_input.toPlainText()
            
            if not all([data, key, signature]):
                QMessageBox.warning(self, "Warning", "Please enter all fields!")
                return
                
            is_valid = verify_hash_hmac(data, signature, key.encode())
            self.hmac_result.setText(f"HMAC Verification {'Successful' if is_valid else 'Failed'}")
            self.hmac_result.setStyleSheet(
                "color: green;" if is_valid else "color: red;"
            )
            self.add_to_history("HMAC", f"Verified HMAC for: {data[:20]}...")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to verify HMAC: {str(e)}")

    def verify_key_action(self):
        """Verify a public key's format and validity"""
        try:
            key = self.verify_key_input.toPlainText()
            if not key:
                QMessageBox.warning(self, "Warning", "Please enter a public key to verify!")
                return
                
            # Basic format validation
            if not key.startswith("-----BEGIN PUBLIC KEY-----") or not key.endswith("-----END PUBLIC KEY-----"):
                self.key_verify_result.setText("Invalid key format")
                self.key_verify_result.setStyleSheet("color: red;")
                return
                
            # Try to load the key
            try:
                from cryptography.hazmat.primitives import serialization
                from cryptography.hazmat.backends import default_backend
                serialization.load_pem_public_key(
                    key.encode(),
                    backend=default_backend()
                )
                self.key_verify_result.setText("Key is valid")
                self.key_verify_result.setStyleSheet("color: green;")
                self.add_to_history("Key Verify", "Verified public key format")
            except Exception as e:
                self.key_verify_result.setText(f"Invalid key: {str(e)}")
                self.key_verify_result.setStyleSheet("color: red;")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to verify key: {str(e)}")
            
    def generate_hmac_action(self):
        """Generate HMAC for the input data"""
        try:
            data = self.hmac_gen_data_input.toPlainText()
            key = self.hmac_gen_key_input.toPlainText()
            
            if not data or not key:
                QMessageBox.warning(self, "Warning", "Please enter both data and key!")
                return
                
            signature = hmac.new(key.encode(), data.encode(), hashlib.sha256).hexdigest()
            self.hmac_gen_output.setText(signature)
            self.add_to_history("HMAC Generate", f"Generated HMAC for: {data[:20]}...")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate HMAC: {str(e)}")
            
    def select_file_to_sign(self):
        """Open file dialog to select a file for signing"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File to Sign",
            "",
            "All Files (*.*)"
        )
        if file_path:
            self.file_path_display.setText(file_path)
            
    def select_file_to_verify(self):
        """Open file dialog to select a file for verification"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File to Verify",
            "",
            "All Files (*.*)"
        )
        if file_path:
            self.verify_file_path_display.setText(file_path)
            
    def sign_file_action(self):
        """Sign the selected file"""
        if not self.private_key:
            QMessageBox.warning(self, "Warning", "Please generate keys first!")
            return
            
        try:
            file_path = self.file_path_display.text()
            if file_path == "No file selected":
                QMessageBox.warning(self, "Warning", "Please select a file first!")
                return
                
            with open(file_path, "rb") as f:
                data = f.read()
                
            signature = sign_data(data, self.private_key)
            self.file_signature_display.setText(signature)
            self.add_to_history("File Sign", f"Signed file: {os.path.basename(file_path)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to sign file: {str(e)}")
            
    def verify_file_action(self):
        """Verify the selected file's signature"""
        if not self.public_key:
            QMessageBox.warning(self, "Warning", "Please generate keys first!")
            return
            
        try:
            file_path = self.verify_file_path_display.text()
            signature = self.verify_file_signature_input.toPlainText()
            
            if file_path == "No file selected":
                QMessageBox.warning(self, "Warning", "Please select a file first!")
                return
                
            if not signature:
                QMessageBox.warning(self, "Warning", "Please enter the signature to verify!")
                return
                
            with open(file_path, "rb") as f:
                data = f.read()
                
            # Convert signature from base64
            signature_bytes = base64.b64decode(signature)
            
            is_valid = verify_signature(data, signature_bytes, self.public_key)
            self.file_verify_result.setText(f"Verification {'Successful' if is_valid else 'Failed'}")
            self.file_verify_result.setStyleSheet(
                "color: green;" if is_valid else "color: red;"
            )
            self.add_to_history("File Verify", f"Verified file: {os.path.basename(file_path)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to verify file: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = CryptoGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 