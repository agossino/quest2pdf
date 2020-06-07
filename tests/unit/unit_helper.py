import os

EXAM_FROM_CONF_INI = "Exam from conf.ini"


def save_app_configuration(file_path):
    text = "[Default]\n"
    file_path.write_text(text)


def save_app_configuration_set(file_path):
    text = f"[Default]\nnumber = 3\nexam = {EXAM_FROM_CONF_INI}\n"
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


def fd_input(prompt: str) -> str:
    with os.fdopen(os.dup(1), "w") as fout:
        fout.write(f"\n{prompt} ")

    with os.fdopen(os.dup(2), "r") as fin:
        return fin.readline()


def save_mono_question_data(file_path):
    text = "question,subject,image,A,B,C,D,void\nQ1,S1,I1,a,b,c,d,\nQ2,S2,I2,a,b,c,d,"
    file_path.write_text(text)
