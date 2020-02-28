def save_app_configuration(file_path):
    text = "[Default]\n"
    file_path.write_text(text)


def save_log_configuration(file_path):
    text = """{
    "disable_existing_loggers": false,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        },
        "file": {
             "level": "DEBUG",
             "class": "logging.handlers.RotatingFileHandler",
             "formatter": "default",
             "filename": "application.log",
             "maxBytes": 1024000,
             "backupCount": 3
        }
    },
    "loggers": {
        "": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": true
        }
    },
    "version": 1
}"""
    file_path.write_text(text)
