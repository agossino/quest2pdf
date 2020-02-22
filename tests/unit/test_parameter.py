import parameter

def test_parser():
    parser = parameter.param_parser()
    expected = {"input": "domande.csv",
                "number": 1,
                "exam": "Esame"}

    assert parser == expected
