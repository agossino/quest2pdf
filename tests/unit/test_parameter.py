import logging
import parameter
from unit_helper import save_log_configuration


def test_default(caplog):
    """test no arguments on command line
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
    assert caplog.record_tuples[0][1] == logging.INFO


def test_cli_set1(tmp_path, caplog):
    """test """
    input_arg = "my_questions.csv"
    log_configuration_file = tmp_path / "loggingConf.json"
    expected = {"input": input_arg,
                "number": 1,
                "exam": "Exam",
                "correction": "Correction",
                "app_configuration_file": "conf.ini",
                "log_configuration_file": str(log_configuration_file),
                "page_heading": False,
                "encoding": "utf-8",
                "delimiter": ",",
                "shuffle": False}
    log_configuration_file = tmp_path / expected["log_configuration_file"]
    save_log_configuration(log_configuration_file)
    parsed = parameter.param_parser([input_arg,
                                     "--log_configuration_file",
                                     str(log_configuration_file)])

    assert parsed == expected
    assert caplog.record_tuples == []

    caplog.clear()


def test_cli_set2():
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
