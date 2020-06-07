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


def save_empty_question(file_path):
    text = "question,subject,image,level,A,Ai,B,Bi,C,Ci\n "
    file_path.write_text(text)


def save_tf_question(file_path):
    text = """Question type,question,A,B,void
TrueFalse,Q,,1,"""
    file_path.write_text(text)


def save_question_data(file_path):
    text = "question,subject,image,level,A,Ai,B,Bi,C,Ci\nQ,S,I,1,a,ai,b,bi,c,ci"
    file_path.write_text(text)
