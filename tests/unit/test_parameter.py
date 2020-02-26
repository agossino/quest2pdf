import logging
import parameter
from unit_helper import save_log_configuration


def test_default(caplog):
    """test no arguments on command line
    amd no logging configuration  file found
    """
    parsed = parameter.param_parser([])
    expected = {"input": "questions.csv",
                "number": 1,
                "exam": "Exam",
                "correction": "Correction",
                "app_configuration_file": "conf.ini",
                "log_configuration_file": "loggingConf.json",
                "page_heading": False,
                "encoding": "utf-8",
                "delimiter": ",",
                "shuffle": False}

    assert parsed == expected
    assert caplog.record_tuples[3][1] == logging.WARNING


def test_cli_set1(tmp_path, caplog, monkeypatch):
    """test logging configuration file in current dir
    """
    input_arg = "my_questions.csv"
    log_configuration_file = "loggingConf.json"
    expected = {"input": input_arg,
                "number": 1,
                "exam": "Exam",
                "correction": "Correction",
                "app_configuration_file": "conf.ini",
                "log_configuration_file": log_configuration_file,
                "page_heading": False,
                "encoding": "utf-8",
                "delimiter": ",",
                "shuffle": False}
    monkeypatch.chdir(tmp_path)
    save_log_configuration(tmp_path / log_configuration_file)
    parsed = parameter.param_parser([input_arg,
                                     "--log_configuration_file",
                                     log_configuration_file])

    assert parsed == expected


def test_cli_set3(tmp_path, caplog, monkeypatch):
    """test logging configuration file in HOME dir
    """
    input_arg = "my_questions.csv"
    log_configuration_file = "loggingConf.json"
    expected = {"input": input_arg,
                "number": 1,
                "exam": "Exam",
                "correction": "Correction",
                "app_configuration_file": "conf.ini",
                "log_configuration_file": log_configuration_file,
                "page_heading": False,
                "encoding": "utf-8",
                "delimiter": ",",
                "shuffle": False}
    monkeypatch.setenv("HOME", str(tmp_path))
    save_log_configuration(tmp_path / log_configuration_file)
    parsed = parameter.param_parser([input_arg,
                                     "--log_configuration_file",
                                     log_configuration_file])

    assert parsed == expected
    assert caplog.record_tuples[0][1] == logging.INFO
    assert caplog.record_tuples[1][1] == logging.INFO


def test_cli_set4():
    option = "--correction"
    param = "my_correction"
    parsed = parameter.param_parser([option, param])
    expected = {"input": "questions.csv",
                "number": 1,
                "exam": "Exam",
                "correction": param,
                "app_configuration_file": "conf.ini",
                "log_configuration_file": "loggingConf.json",
                "page_heading": False,
                "encoding": "utf-8",
                "delimiter": ",",
                "shuffle": False}

    assert parsed == expected
