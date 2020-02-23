import parameter


def test_default():
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


def test_cli_set1():
    input_arg = "my_questions.csv"
    parsed = parameter.param_parser([input_arg])
    expected = {"input": input_arg,
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
