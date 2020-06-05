import logging
import pathlib
import pytest
import parameter
from unit_helper import (
    save_app_configuration,
    save_app_configuration_set,
    save_log_configuration,
)


def test_default0(caplog):
    """test no logging configuration and
    no app configuration file found
    """
    parameter.param_parser([])

    assert caplog.record_tuples[3][1] == logging.WARNING
    assert caplog.record_tuples[7][1] == logging.WARNING


def test_default1(tmp_path, caplog, monkeypatch):
    """test no arguments on command line
    amd no logging configuration file found;
    app configuration file in current dir
    """
    expected = {
        "input": "questions.csv",
        "number": 1,
        "exam": "Exam",
        "correction": "Correction",
        "app_configuration_file": "conf.ini",
        "log_configuration_file": "loggingConf.json",
        "page_heading": False,
        "page_footer": False,
        "encoding": "utf-8",
        "delimiter": ",",
        "not_shuffle": True,
    }

    monkeypatch.chdir(tmp_path)

    app_configuration_file = expected["app_configuration_file"]
    save_app_configuration(tmp_path / app_configuration_file)

    param = parameter.param_parser([])

    assert param == expected
    assert len(caplog.record_tuples) == 5


def test_default2(tmp_path, caplog, monkeypatch):
    """test no arguments on command line,
    no logging configuration file found,
    app configuration file in script dir
    """
    expected = {
        "input": "questions.csv",
        "number": 1,
        "exam": "Exam",
        "correction": "Correction",
        "app_configuration_file": "conf.ini",
        "log_configuration_file": "loggingConf.json",
        "page_heading": False,
        "page_footer": False,
        "encoding": "utf-8",
        "delimiter": ",",
        "not_shuffle": True,
    }

    mock_path = tmp_path
    monkeypatch.setattr(pathlib.Path, "parent", mock_path)

    app_configuration_file = expected["app_configuration_file"]
    save_app_configuration(tmp_path / app_configuration_file)

    param = parameter.param_parser([])

    assert param == expected
    assert len(caplog.record_tuples) == 6


def test_default3(tmp_path, caplog, monkeypatch):
    """test no arguments on command line,
    no logging configuration file found,
    app configuration file in home dir
    """
    expected = {
        "input": "questions.csv",
        "number": 1,
        "exam": "Exam",
        "correction": "Correction",
        "app_configuration_file": "conf.ini",
        "log_configuration_file": "loggingConf.json",
        "page_heading": False,
        "page_footer": False,
        "encoding": "utf-8",
        "delimiter": ",",
        "not_shuffle": True,
    }

    monkeypatch.setenv("HOME", str(tmp_path))

    app_configuration_file = expected["app_configuration_file"]
    save_app_configuration(tmp_path / app_configuration_file)

    param = parameter.param_parser([])

    assert param == expected
    assert len(caplog.record_tuples) == 7


def test_default4(tmp_path, caplog, monkeypatch):
    """test app configuration given as argument but no file saved
    no logging configuration
    """
    file_name = "conf.ini"
    app_configuration_file = str(pathlib.Path.home() / file_name)

    parameter.param_parser(["app_configuration_file", app_configuration_file])

    assert caplog.record_tuples[3][1] == logging.WARNING
    assert file_name in caplog.record_tuples[4][2]
    assert file_name in caplog.record_tuples[5][2]
    assert file_name in caplog.record_tuples[6][2]
    assert caplog.record_tuples[7][1] == logging.WARNING


def test_default5(tmp_path, monkeypatch):
    """test log and app configuration file in current dir
    """
    expected = {
        "input": "questions.csv",
        "number": 1,
        "exam": "Exam",
        "correction": "Correction",
        "app_configuration_file": "conf.ini",
        "log_configuration_file": "loggingConf.json",
        "page_heading": False,
        "page_footer": False,
        "encoding": "utf-8",
        "delimiter": ",",
        "not_shuffle": True,
    }

    log_file = tmp_path / "application.log"
    monkeypatch.chdir(tmp_path)

    app_configuration_file = expected["app_configuration_file"]
    save_app_configuration(tmp_path / app_configuration_file)
    log_configuration_file = expected["log_configuration_file"]
    save_log_configuration(tmp_path / log_configuration_file)

    param = parameter.param_parser([])

    assert param == expected
    assert log_file.exists()


def test_default6(tmp_path, monkeypatch):
    """test log and app configuration file in script dir
    """
    expected = {
        "input": "questions.csv",
        "number": 1,
        "exam": "Exam",
        "correction": "Correction",
        "app_configuration_file": "conf.ini",
        "log_configuration_file": "loggingConf.json",
        "page_heading": False,
        "page_footer": False,
        "encoding": "utf-8",
        "delimiter": ",",
        "not_shuffle": True,
    }

    script_dir = tmp_path / "script_dir"
    script_dir.mkdir()
    mock_path = script_dir
    monkeypatch.setattr(pathlib.Path, "parent", mock_path)
    log_file = tmp_path / "application.log"
    monkeypatch.chdir(tmp_path)

    app_configuration_file = expected["app_configuration_file"]
    save_app_configuration(script_dir / app_configuration_file)
    log_configuration_file = expected["log_configuration_file"]
    save_log_configuration(script_dir / log_configuration_file)

    param = parameter.param_parser([])

    assert param == expected
    assert log_file.exists()


def test_default7(tmp_path, monkeypatch):
    """test log and app configuration file in home dir
    """
    expected = {
        "input": "questions.csv",
        "number": 1,
        "exam": "Exam",
        "correction": "Correction",
        "app_configuration_file": "conf.ini",
        "log_configuration_file": "loggingConf.json",
        "page_heading": False,
        "page_footer": False,
        "encoding": "utf-8",
        "delimiter": ",",
        "not_shuffle": True,
    }

    home_dir = tmp_path / "home_dir"
    home_dir.mkdir()
    monkeypatch.setenv("HOME", str(home_dir))
    log_file = tmp_path / "application.log"
    monkeypatch.chdir(tmp_path)

    app_configuration_file = expected["app_configuration_file"]
    save_app_configuration(home_dir / app_configuration_file)
    log_configuration_file = expected["log_configuration_file"]
    save_log_configuration(home_dir / log_configuration_file)

    param = parameter.param_parser([])

    assert param == expected
    assert log_file.exists()


def test_cli_set1(tmp_path, monkeypatch):
    """test arguments: argument has precedence on config file (number),
    config file has precedence on default (exam)
    """
    expected = {
        "input": "my_questions.csv",
        "number": 2,
        "exam": "my exam",
        "correction": "Correction",
        "app_configuration_file": "conf.ini",
        "log_configuration_file": "loggingConf.json",
        "page_heading": False,
        "page_footer": False,
        "encoding": "utf-8",
        "delimiter": ",",
        "not_shuffle": True,
    }

    monkeypatch.chdir(tmp_path)
    app_configuration_file = expected["app_configuration_file"]
    save_app_configuration_set(tmp_path / app_configuration_file)
    log_configuration_file = expected["log_configuration_file"]
    save_log_configuration(tmp_path / log_configuration_file)
    parsed = parameter.param_parser(
        ["input", expected["input"], "number", expected["number"]]
    )

    assert parsed == expected
