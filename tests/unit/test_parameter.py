import logging
import pathlib

import parameter
from unit_helper import (
    save_app_configuration,
    save_app_configuration_set,
    save_log_configuration,
)


def test_no_files(caplog, monkeypatch, tmp_path):
    """no logging configuration and
    no app configuration file found warning: 2 warnings
    """
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pathlib.Path, "parent", tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path))
    parameter.param_parser([])

    warning_log_levels = [
        item[1] for item in caplog.record_tuples if item[1] == logging.WARNING
    ]

    assert len(warning_log_levels) == 2


def test_app_file_curr_dir(tmp_path, caplog, monkeypatch):
    """test default values;
    no logging configuration file found;
    app configuration file in current dir: 1 warning
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

    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    monkeypatch.setattr(pathlib.Path, "parent", empty_dir)
    monkeypatch.setenv("HOME", str(empty_dir))
    monkeypatch.chdir(tmp_path)

    app_configuration_file = expected["app_configuration_file"]
    save_app_configuration(tmp_path / app_configuration_file)

    param = parameter.param_parser([])

    warning_log_levels = [
        item[1] for item in caplog.record_tuples if item[1] == logging.WARNING
    ]

    assert param == expected
    assert len(warning_log_levels) == 1


def test_app_file_script_dir(tmp_path, caplog, monkeypatch):
    """no logging configuration file found,
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

    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    monkeypatch.chdir(empty_dir)
    monkeypatch.setenv("HOME", str(empty_dir))
    monkeypatch.setattr(pathlib.Path, "parent", tmp_path)

    app_configuration_file = expected["app_configuration_file"]
    save_app_configuration(tmp_path / app_configuration_file)

    param = parameter.param_parser([])

    warning_log_levels = [
        item[1] for item in caplog.record_tuples if item[1] == logging.WARNING
    ]

    assert param == expected
    assert len(warning_log_levels) == 1


def test_app_file_home_dir(tmp_path, caplog, monkeypatch):
    """test no given arguments,
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

    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    monkeypatch.chdir(empty_dir)
    monkeypatch.setattr(pathlib.Path, "parent", empty_dir)
    monkeypatch.setenv("HOME", str(tmp_path))

    app_configuration_file = expected["app_configuration_file"]
    save_app_configuration(tmp_path / app_configuration_file)

    param = parameter.param_parser([])

    warning_log_levels = [
        item[1] for item in caplog.record_tuples if item[1] == logging.WARNING
    ]

    assert param == expected
    assert len(warning_log_levels) == 1


def test_log_file_curr_dir(tmp_path, monkeypatch):
    """logging configuration file in current dir found;
    no app configuration file: 1 warning.
    """
    expected = {
        "app_configuration_file": "conf.ini",
        "log_configuration_file": "loggingConf.json"
    }

    home_dir = tmp_path / "home_empty"
    home_dir.mkdir()
    monkeypatch.setenv("HOME", str(home_dir))

    script_dir = tmp_path / "script_empty"
    script_dir.mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pathlib.Path, "parent", script_dir)

    log_configuration_file = expected["log_configuration_file"]
    save_log_configuration(tmp_path / log_configuration_file)

    parameter.param_parser([])

    log_file = tmp_path / "application.log"
    with log_file.open() as fd:
        log_content = fd.readlines()

    assert "".join(log_content).count(logging.getLevelName(logging.WARNING)) == 1


def test_log_file_script_dir(tmp_path, caplog, monkeypatch):
    """test no arguments on command line,
    logging configuration file in script dir found,
    no app configuration file: 1 warning.
    """
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    monkeypatch.chdir(empty_dir)
    monkeypatch.setenv("HOME", str(empty_dir))

    monkeypatch.setattr(pathlib.Path, "parent", tmp_path)

    log_configuration_file = "loggingConf.json"
    save_log_configuration(tmp_path / log_configuration_file)

    parameter.param_parser([])

    warning_log_levels = [
        item[1] for item in caplog.record_tuples if item[1] == logging.WARNING
    ]

    assert len(warning_log_levels) == 1


def test_log_file_home_dir(tmp_path, capsys, monkeypatch):
    """test no arguments on command line,
    logging configuration file in home dir found,
    no app configuration file: 1 warning.
    """
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    monkeypatch.chdir(empty_dir)
    monkeypatch.setattr(pathlib.Path, "parent", empty_dir)

    monkeypatch.setenv("HOME", str(tmp_path))

    log_configuration_file = "loggingConf.json"
    save_log_configuration(tmp_path / log_configuration_file)

    parameter.param_parser([])

    captured = capsys.readouterr()
    warning_log_levels = [
        1 for line in captured.out.split("\n") if line.find("WARNING") != -1
    ]

    assert warning_log_levels == [1]


def test_cli_app_conf_wo_file(tmp_path, caplog, monkeypatch):
    """test app configuration path in command line but no file saved
    no logging configuration
    """
    app_configuration_file = str(pathlib.Path.home() / "conf.ini")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(pathlib.Path, "parent", tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path))

    parameter.param_parser(["--app_configuration_file", app_configuration_file])

    warning_log_levels = [
        item[1] for item in caplog.record_tuples if item[1] == logging.WARNING
    ]

    assert len(warning_log_levels) == 2


def test_log_output(tmp_path, monkeypatch):
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

    output_log_file = tmp_path / "application.log"
    monkeypatch.chdir(tmp_path)

    app_configuration_file = expected["app_configuration_file"]
    save_app_configuration(tmp_path / app_configuration_file)
    log_configuration_file = expected["log_configuration_file"]
    save_log_configuration(tmp_path / log_configuration_file)

    param = parameter.param_parser([])

    assert param == expected
    assert output_log_file.exists()


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


def test_default4_given_arg(tmp_path, caplog, monkeypatch):
    """test app configuration given as argument but no file saved
    no logging configuration: 2 warnings
    """
    file_name = "conf.ini"
    app_configuration_file = str(tmp_path / file_name)

    parameter.param_parser(["app_configuration_file", app_configuration_file])

    warning_log_levels = [
        item[1] for item in caplog.record_tuples if item[1] == logging.WARNING
    ]

    assert len(warning_log_levels) == 2


def test_files_in_script_dir(tmp_path, monkeypatch):
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


def test_files_in_home_dir(tmp_path, monkeypatch):
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


