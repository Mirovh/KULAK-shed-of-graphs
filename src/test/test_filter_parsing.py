import pytest
import json
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))
import plantriFilter as pf


@pytest.fixture
def setup():
    with open("./resources/RuleTarget.json", "r") as file:
        targetJson = json.load(file)
    with open("./resources/RuleTargetMultipleDegrees.json", "r") as file:
        targetJsonMultipleDegrees = json.load(file)

    yield targetJson, targetJsonMultipleDegrees   # Run the test

    targetJson = None
    targetJsonMultipleDegrees = None


def test_parse_string_correct_full(setup):
    targetJson, _ = setup
    # Tests a string containing all the rules split by "and" with various capitalizations
    filter_string = "maximum 3 vertices with degree 2 and minimum 1 vertices with degree 3 and exactly 2 vertices with degree 4 and only vertices with degree 5"
    filter_json = pf.parse_string(filter_string)
    assert filter_json == targetJson
    filter_string = "Maximum 3 vertices with degree 2 and Minimum 1 vertices with degree 3 and Exactly 2 vertices with degree 4 and Only vertices with degree 5"
    filter_json = pf.parse_string(filter_string)
    assert filter_json == targetJson
    filter_string = "Maximum 3 vertices with degree 2 And Minimum 1 vertices with degree 3 And Exactly 2 vertices with degree 4 And Only vertices with degree 5"
    filter_json = pf.parse_string(filter_string)
    assert filter_json == targetJson

def test_parse_string_correct_single():
    filter_string = "maximum 3 vertices with degree 2"
    filter_json = pf.parse_string(filter_string)
    assert filter_json == {"rules": [{"rule": "max", "degrees": [2], "count": 3}]}

def test_parse_string_float():
    filter_string = "maximum 3.5 vertices with degree 2"
    with pytest.raises(pf.FilterStringError):
        pf.parse_string(filter_string)
    filter_string = "maximum 3,5 vertices with degree 2"
    with pytest.raises(pf.FilterStringError):
        pf.parse_string(filter_string)

def test_parse_string_incorrect():
    filter_string = "nonsense 2 to 3 and 5"
    with pytest.raises(pf.FilterStringError):
        pf.parse_string(filter_string)

def test_parse_string_empty():
    filter_string = ""
    with pytest.raises(pf.FilterStringError):
        pf.parse_string(filter_string)

def test_parse_string_no_and():
    filter_string = "maximum 3 vertices with degree 2 minimum 1 vertices with degree 3 exactly 2 vertices with degree 4 only vertices with degree 5"
    with pytest.raises(pf.FilterStringError):
        pf.parse_string(filter_string)
        
def test_parse_string_multiple_degrees():
    filter_string = "maximum 3 vertices with degree 2 or 3"
    filter_json = pf.parse_string(filter_string)
    assert filter_json == {"rules": [{"rule": "max", "degrees": [2, 3], "count": 3}]}
    filter_string = "minimum 3 vertices with degree 2 or 3 or 4"
    filter_json = pf.parse_string(filter_string)
    assert filter_json == {"rules": [{"rule": "min", "degrees": [2, 3, 4], "count": 3}]}
    filter_string = "exactly 3 vertices with degree 2 or 3 or 4"
    filter_json = pf.parse_string(filter_string)
    assert filter_json == {"rules": [{"rule": "exact", "degrees": [2, 3, 4], "count": 3}]}
    filter_string = "only vertices with degree 2 or 3 or 4"
    filter_json = pf.parse_string(filter_string)
    assert filter_json == {"rules": [{"rule": "only", "degrees": [2, 3, 4]}]}

def test_parse_string_multiple_rules_multiple_degrees(setup):
    _, targetJsonMultipleDegrees = setup
    filter_string = "maximum 3 vertices with degree 2 or 3 and minimum 1 vertices with degree 3 or 4 and exactly 2 vertices with degree 4 or 5 and only vertices with degree 5 or 6"
    filter_json = pf.parse_string(filter_string)
    assert filter_json == targetJsonMultipleDegrees
    
def test_parse_string_or():
    filter_string = "maximum 3 vertices with degree 2 or "
    with pytest.raises(pf.FilterStringError):
        pf.parse_string(filter_string)
    filter_string = "maximum 3 vertices with degree 2 or"
    with pytest.raises(pf.FilterStringError):
        pf.parse_string(filter_string)
    filter_string = "maximum 3 vertices with degree 2 or and"
    with pytest.raises(pf.FilterStringError):
        pf.parse_string(filter_string)
    filter_string = "maximum 3 vertices with degree 2 or and 3"
    with pytest.raises(pf.FilterStringError):
        pf.parse_string(filter_string)