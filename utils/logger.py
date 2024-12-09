import logging
import json
from datetime import datetime
from config.settings import settings


class JsonLogger:
    """Custom JSON logger for structured logging."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        handler = logging.StreamHandler()
        handler.setLevel(log_level)
        handler.setFormatter(self.JsonFormatter())
        self.logger.addHandler(handler)

    class JsonFormatter(logging.Formatter):
        """Formats log records as JSON."""

        def format(self, record):
            log_record = {
                "timestamp": datetime.utcnow().isoformat(),
                "level": record.levelname,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
                "extra": getattr(record, 'extra', {})
            }
            return json.dumps(log_record)

    def debug(self, message: str, **context):
        self.logger.debug(message, extra={'extra': context})

    def info(self, message: str, **context):
        self.logger.info(message, extra={'extra': context})

    def warning(self, message: str, **context):
        self.logger.warning(message, extra={'extra': context})

    def error(self, message: str, **context):
        self.logger.error(message, extra={'extra': context})

    def critical(self, message: str, **context):
        self.logger.critical(message, extra={'extra': context})


# Initialize a global logger instance
app_logger = JsonLogger("NebuloViz")
