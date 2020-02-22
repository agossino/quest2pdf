import parameter

def test_parser():
    parsed = parameter.param_parser([])
    expected = {"input": "domande.csv",
                "number": 1,
                "exam": "Esame",
                "correction": "Correttore",
                "conffile": "conf.ini",
                "conflogfile": "loggingConf.json",
                "page_heading": False,
                "encoding": "utf-8",
                "delimiter": ",",
                "shuffle": False}

    assert parsed == expected
