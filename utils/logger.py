import logging
import logging.handlers
from config.settings import LOGS_DIR, LOG_LEVEL

# Create logger
logger = logging.getLogger("RecruitFlow")
logger.setLevel(LOG_LEVEL)

# File handler with rotation
log_file = LOGS_DIR / "recruitflow.log"
file_handler = logging.handlers.RotatingFileHandler(
    log_file,
    maxBytes=10 * 1024 * 1024,  # 10MB
    backupCount=10
)
file_handler.setLevel(LOG_LEVEL)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)