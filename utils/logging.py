import hashlib
import logging
from logging.handlers import RotatingFileHandler

class ImmutableLogHandler(RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.previous_hash = hashlib.sha256(b"GENESIS").hexdigest()

    def emit(self, record):
        record.msg = f"{record.msg} | PrevHash: {self.previous_hash}"
        super().emit(record)
        # Calculate new hash based on the log entry
        self.previous_hash = hashlib.sha256(f"{self.previous_hash}{record.msg}".encode()).hexdigest()

def setup_logger():
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Setup file handler
    file_handler = ImmutableLogHandler('app_activity.log', maxBytes=10000, backupCount=3)
    file_handler.setFormatter(formatter)
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Setup logger
    logger = logging.getLogger('app_logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 