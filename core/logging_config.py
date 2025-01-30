import logging


class MediMeetLogger:
    """
    A custom logger class for handling different logging levels and formats.
    """
    _instance = None  # Class-level attribute to hold the singleton instance

    def __new__(cls, name=None):
        """
        This method is called when a new object is created. It ensures that
        only one instance of the logger is created (singleton pattern).
        """
        if cls._instance is None:
            # Create a new instance only if it doesn't exist
            cls._instance = super().__new__(cls)
            cls._instance.logger = logging.getLogger(name or __name__)
            cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self):
        """
        Setup logging configuration.
        """
        self.logger.setLevel(logging.DEBUG)  # Default log level
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # File handler (optional)
        file_handler = logging.FileHandler('app.log')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        """
        Log a message with level DEBUG.
        """
        self.logger.debug(message)

    def info(self, message):
        """
        Log a message with level INFO.
        """
        self.logger.info(message)

    def warning(self, message):
        """
        Log a message with level WARNING.
        """
        self.logger.warning(message)

    def error(self, message):
        """
        Log a message with level ERROR.
        """
        self.logger.error(message)

    def critical(self, message):
        """
        Log a message with level CRITICAL.
        """
        self.logger.critical(message)


# Global logger instance (the singleton object) that can be used throughout the app
medimeetlogger = MediMeetLogger()
