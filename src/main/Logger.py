import logging
import os
from datetime import datetime

class Logger:
    _instance = None
    _initialized = False
    
    # ANSI 顏色代碼
    RED = '\033[91m'
    RESET = '\033[0m'
    
    DEFAULT_LOG_DIR = "./logs"
    ERROR_FORMAT = f'{RED}[%(asctime)s] [%(levelname)8s] %(filename)s:%(lineno)d - %(message)s{RESET}'
    INFO_FORMAT = '[%(asctime)s] [%(levelname)8s] %(message)s'
    LOGGER_NAME = 'IDCardLogger'

    def __new__(cls, log_dir=DEFAULT_LOG_DIR):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self, log_dir=DEFAULT_LOG_DIR):
        if not Logger._initialized:
            self._setup_log_directory(log_dir)
            self._setup_logger()
            Logger._initialized = True
    
    def _setup_log_directory(self, log_dir):
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(
            log_dir, 
            f"idcard_{datetime.now().strftime('%Y%m%d')}.log"
        )
    
    def _setup_logger(self):
        self.logger = logging.getLogger(self.LOGGER_NAME)
        self.logger.propagate = False
        
        if not self.logger.handlers:
            self._configure_logger()
    
    def _configure_logger(self):
        self.logger.setLevel(logging.INFO)
        
        # 為 INFO 和 ERROR 創建不同的 handler
        info_handler = self._create_handler(self.INFO_FORMAT)
        error_handler = self._create_handler(self.ERROR_FORMAT)
        
        # 設置 handler 的級別過濾
        info_handler.setLevel(logging.INFO)
        info_handler.addFilter(lambda record: record.levelno == logging.INFO)
        
        error_handler.setLevel(logging.ERROR)
        
        self.logger.addHandler(info_handler)
        self.logger.addHandler(error_handler)
    
    def _create_handler(self, fmt):
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        return handler
            
    def info(self, message):
        self.logger.info(message)
    
    def error(self, message):
        self.logger.error(message)