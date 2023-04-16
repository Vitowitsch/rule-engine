from rule_engine.rule_engine import RuleEngine
import pandas as pd


def test_expr_parser():
    """Parse boolean expressions."""
    data = [{'objectid': 't1', 'event_date': '2021-03-02', 'mean_0815': 10, 'mean_007': -1},
            {'objectid': 't1', 'event_date': '2021-03-02', 'mean_0815': 10, 'mean_007': +1}]
    df = pd.DataFrame(data)
    param = {"Expression": "mean_0815 < 11 and mean_007 > 0", "ResponseValue": True, "ResponseDefault": False, "MinimumDaysRequired": 1,
             "ResponseColumn": "anomaly", "DefaultClass": ""
             }
    re = RuleEngine(param)
    result = re.apply(df)['anomaly']
    assert False == result[0]
    assert True == result[1]


def test_original_rules():
    """Parse boolean expressions."""
    data = [{'2597': 2.0, 'rm2597': 2.0, 'rm2372_1': 0.0, 'rm2572_1': 0.0,
             'rm2372_5': 0.0, 'rm2374': 0.0, 'rm2395': 0.0}]
    df = pd.DataFrame(data)
    param = {
        "Expression": "(rm2597 > (rm2372_1 * 1.5)) or (rm2372_5 >= 1 and rm2374 > 0 and rm2395 !=1)", "ResponseValue": True, "ResponseDefault": False, "MinimumDaysRequired": 1,
        "ResponseColumn": "anomaly"}
    re = RuleEngine(param)
    result = re.apply(df)['anomaly']
    assert True == result[0]


def test_classification_true():
    """Parse boolean expressions."""
    data = [{'rm2597': 2.0, 'rm2372': 1.0}]
    responseCol = 'anomalyclass'
    responseVal = 'classA'
    df = pd.DataFrame(data)
    param = {
        "Expression": "rm2597 * 1.5 >  rm2372",  "ResponseValue": responseVal, "ResponseDefault": False, "ResponseColumn": responseCol, "MinimumDaysRequired": 1, }
    re = RuleEngine(param)
    result = re.apply(df)[responseCol]

    assert responseVal == result[0]


def test_classification_false():
    """Parse boolean expressions."""
    responseCol = 'anomalyclass'
    responseVal = 'classA'

    data = [{'rm2597': 2.0, 'rm2372': 4.0}]
    df = pd.DataFrame(data)
    param = {
        "Expression": "rm2597 * 1.5 >  rm2372",  "ResponseValue": responseVal, "ResponseColumn": responseCol, "ResponseDefault": False, "MinimumDaysRequired": 5, }

    re = RuleEngine(param)
    result = re.apply(df)[responseCol]
    assert responseVal != result[0]


def test_not_enough_data():
    """Parse boolean expressions."""
    responseCol = 'anomalyclass'
    responseVal = 'classA'

    data = [{'rm2597': 2.0, 'rm2372': 4.0}]
    df = pd.DataFrame(data)
    param = {
        "Expression": "rm2597 * 1.5 >  rm2372",  "ResponseValue": responseVal, "ResponseColumn": responseCol, "ResponseDefault": False, "MinimumDaysRequired": 2, }

    re = RuleEngine(param)
    result = re.apply(df)[responseCol]
    assert result[0] == RuleEngine.not_enough_data_available


