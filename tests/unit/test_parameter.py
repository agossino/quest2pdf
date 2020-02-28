import logging
import pathlib
from collections import namedtuple
import pytest
import parameter
from unit_helper import save_log_configuration, save_app_configuration


def test_default0(caplog, monkeypatch):
    """test no arguments on command line
    amd no logging configuration and
    no app configuration file found
    """
    with pytest.raises(FileNotFoundError):
        parameter.param_parser([])

    assert caplog.record_tuples[3][1] == logging.WARNING


def test_default1(tmp_path, caplog, monkeypatch):
    """test no arguments on command line
    amd no logging configuration file found;
    app configuration file in current dir
    """
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
    app_configuration_file = expected["app_configuration_file"]
    save_app_configuration(tmp_path / app_configuration_file)
    monkeypatch.chdir(tmp_path)
    param = parameter.param_parser([])

    assert param == expected
    assert len(caplog.record_tuples) == 5


def test_default2(tmp_path, caplog, monkeypatch):
    """test no arguments on command line
    amd no logging configuration file found;
    app configuration file in script dir
    """
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

    def resolve(arg):
        Parent = namedtuple("Parent", ["parent"])
        value = Parent(tmp_path)
        return value
    monkeypatch.setattr(pathlib.Path, "resolve", resolve)

    app_configuration_file = expected["app_configuration_file"]
    save_app_configuration(tmp_path / app_configuration_file)
    param = parameter.param_parser([])

    assert param == expected
    assert len(caplog.record_tuples) == 6


def test_default3(tmp_path, caplog, monkeypatch):
    """test no arguments on command line
    amd no logging configuration file found;
    app configuration file in home dir
    """
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

    app_configuration_file = expected["app_configuration_file"]
    save_app_configuration(tmp_path / app_configuration_file)
    monkeypatch.setenv("HOME", str(tmp_path))
    param = parameter.param_parser([])

    assert param == expected
    assert len(caplog.record_tuples) == 7


def test_default4(tmp_path, caplog, monkeypatch):
    """test no arguments on command line
    amd no logging configuration file found;
    app configuration file in home dir
    """
    app_configuration_file = pathlib.Path.home() / "conf.ini"
    expected = {"input": "questions.csv",
                "number": 1,
                "exam": "Exam",
                "correction": "Correction",
                "app_configuration_file": str(app_configuration_file),
                "log_configuration_file": "loggingConf.json",
                "page_heading": False,
                "encoding": "utf-8",
                "delimiter": ",",
                "shuffle": False}

    def resolve(arg):
        Parent = namedtuple("Parent", ["parent"])
        value = Parent(tmp_path)
        return value
    monkeypatch.setattr(pathlib.Path, "resolve", resolve)

    save_app_configuration(tmp_path / app_configuration_file.name)
    param = parameter.param_parser(["--app_configuration_file",
                                    expected["app_configuration_file"]])

    assert param == expected
    assert len(caplog.record_tuples) == 6


def test_default20(tmp_path, monkeypatch):
    """test no arguments on command line
    """
    log_file = tmp_path / "application.log"
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
    app_configuration_file = expected["app_configuration_file"]
    save_app_configuration(tmp_path / app_configuration_file)
    log_configuration_file = expected["log_configuration_file"]
    save_log_configuration(tmp_path / log_configuration_file)
    monkeypatch.chdir(tmp_path)
    param = parameter.param_parser([])

    assert param == expected
    assert log_file.exists()


# def test_cli_set1(tmp_path, caplog, monkeypatch):
#     """test logging configuration file in current dir
#     """
#     expected = {"input": "my_questions.csv",
#                 "number": 1,
#                 "exam": "Exam",
#                 "correction": "Correction",
#                 "app_configuration_file": "conf.ini",
#                 "log_configuration_file": "loggingConf.json",
#                 "page_heading": False,
#                 "encoding": "utf-8",
#                 "delimiter": ",",
#                 "shuffle": False}
#     input_arg = expected["input"]
#     log_configuration_file = expected["log_configuration_file"]
#     save_log_configuration(tmp_path / log_configuration_file)
#     monkeypatch.chdir(tmp_path)
#     parsed = parameter.param_parser([input_arg,
#                                      "--log_configuration_file",
#                                      log_configuration_file])
#
#     assert parsed == expected
#     assert caplog.record_tuples == []


# def test_cli_set3(tmp_path, caplog, monkeypatch):
#     """test logging configuration file in script dir
#     """
#     input_arg = "my_questions.csv"
#     log_configuration_file = "loggingConf.json"
#     app_configuration_file = "conf.ini"
#     expected = {"input": input_arg,
#                 "number": 1,
#                 "exam": "Exam",
#                 "correction": "Correction",
#                 "app_configuration_file": "conf.ini",
#                 "log_configuration_file": log_configuration_file,
#                 "page_heading": False,
#                 "encoding": "utf-8",
#                 "delimiter": ",",
#                 "shuffle": False}
#
#     def resolve(arg):
#         Parent = namedtuple("Parent", ["parent"])
#         value = Parent(tmp_path)
#         return value
#
#     monkeypatch.setattr(pathlib.Path, "resolve", resolve)
#     save_log_configuration(tmp_path / log_configuration_file)
#     save_app_configuration(tmp_path / app_configuration_file)
#     parsed = parameter.param_parser([input_arg,
#                                      "--log_configuration_file",
#                                      log_configuration_file])
#
#     assert parsed == expected
#     assert caplog.record_tuples == []
#
#
# def test_cli_set4(tmp_path, caplog, monkeypatch):
#     """test logging configuration file in HOME dir
#     """
#     input_arg = "my_questions.csv"
#     log_configuration_file = "loggingConf.json"
#     expected = {"input": input_arg,
#                 "number": 1,
#                 "exam": "Exam",
#                 "correction": "Correction",
#                 "app_configuration_file": "conf.ini",
#                 "log_configuration_file": log_configuration_file,
#                 "page_heading": False,
#                 "encoding": "utf-8",
#                 "delimiter": ",",
#                 "shuffle": False}
#     monkeypatch.setenv("HOME", str(tmp_path))
#     save_log_configuration(tmp_path / log_configuration_file)
#     parsed = parameter.param_parser([input_arg,
#                                      "--log_configuration_file",
#                                      log_configuration_file])
#
#     assert parsed == expected
#     assert caplog.record_tuples[0][1] == logging.INFO
#     assert caplog.record_tuples[1][1] == logging.INFO
#
#
# def test_cli_set5():
#     option = "--correction"
#     param = "my_correction"
#     parsed = parameter.param_parser([option, param])
#     expected = {"input": "questions.csv",
#                 "number": 1,
#                 "exam": "Exam",
#                 "correction": param,
#                 "app_configuration_file": "conf.ini",
#                 "log_configuration_file": "loggingConf.json",
#                 "page_heading": False,
#                 "encoding": "utf-8",
#                 "delimiter": ",",
#                 "shuffle": False}
#
#     assert parsed == expected
