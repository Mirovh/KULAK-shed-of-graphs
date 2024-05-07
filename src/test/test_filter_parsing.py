import pytest
import json
import src.app.plantriFilter as pf


@pytest.fixture
def setup(self):
    with open("src/test/resources/RuleTarget.json", "r") as file:
        self.targetJson = json.load(file)
    with open("src/test/resources/RuleTargetMultipleDegrees.json", "r") as file:
        self.targetJsonMultipleDegrees = json.load(file)

    yield   # Run the test

    self.targetJson = None
    self.targetJsonMultipleDegrees = None


def test_parse_string_correct_full(self):
    # Tests a string containing all the rules split by "and" with various capitalizations
    filter_string = "maximum 3 vertices with degree 2 and minimum 1 vertices with degree 3 and exactly 2 vertices with degree 4 and only vertices with degree 5"
    filter_json = pf.parse_string(filter_string)
    self.assertEqual(filter_json, self.targetJson)
    filter_string = "Maximum 3 vertices with degree 2 and Minimum 1 vertices with degree 3 and Exactly 2 vertices with degree 4 and Only vertices with degree 5"
    filter_json = pf.parse_string(filter_string)
    self.assertEqual(filter_json, self.targetJson)
    filter_string = "Maximum 3 vertices with degree 2 And Minimum 1 vertices with degree 3 And Exactly 2 vertices with degree 4 And Only vertices with degree 5"
    filter_json = pf.parse_string(filter_string)
    self.assertEqual(filter_json, self.targetJson)

def test_parse_string_correct_single(self):
    filter_string = "maximum 3 vertices with degree 2"
    filter_json = pf.parse_string(filter_string)
    self.assertEqual(filter_json, {"rules": [{"rule": "max", "degrees": [2], "count": 3}]})

def test_parse_string_float(self):
    filter_string = "maximum 3.5 vertices with degree 2"
    with self.assertRaises(pf.FilterStringError):
        pf.parse_string(filter_string)
    filter_string = "maximum 3,5 vertices with degree 2"
    with self.assertRaises(pf.FilterStringError):
        pf.parse_string(filter_string)

def test_parse_string_incorrect(self):
    filter_string = "nonsense 2 to 3 and 5"
    with self.assertRaises(pf.FilterStringError):
        pf.parse_string(filter_string)

def test_parse_string_empty(self):
    filter_string = ""
    with self.assertRaises(pf.FilterStringError):
        pf.parse_string(filter_string)

def test_parse_string_no_and(self):
    filter_string = "maximum 3 vertices with degree 2 minimum 1 vertices with degree 3 exactly 2 vertices with degree 4 only vertices with degree 5"
    with self.assertRaises(pf.FilterStringError):
        pf.parse_string(filter_string)
        
def test_parse_string_multiple_degrees(self):
    filter_string = "maximum 3 vertices with degree 2 or 3"
    filter_json = pf.parse_string(filter_string)
    self.assertEqual(filter_json, {"rules": [{"rule": "max", "degrees": [2, 3], "count": 3}]})
    filter_string = "minimum 3 vertices with degree 2 or 3 or 4"
    filter_json = pf.parse_string(filter_string)
    self.assertEqual(filter_json, {"rules": [{"rule": "min", "degrees": [2, 3, 4], "count": 3}]})
    filter_string = "exactly 3 vertices with degree 2 or 3 or 4"
    filter_json = pf.parse_string(filter_string)
    self.assertEqual(filter_json, {"rules": [{"rule": "exact", "degrees": [2, 3, 4], "count": 3}]})
    filter_string = "only vertices with degree 2 or 3 or 4"
    filter_json = pf.parse_string(filter_string)
    self.assertEqual(filter_json, {"rules": [{"rule": "only", "degrees": [2, 3, 4]}]})

def test_parse_string_multiple_rules_multiple_degrees(self):
    filter_string = "maximum 3 vertices with degree 2 or 3 and minimum 1 vertices with degree 3 or 4 and exactly 2 vertices with degree 4 or 5 and only vertices with degree 5 or 6"
    filter_json = pf.parse_string(filter_string)
    self.assertEqual(filter_json, self.targetJsonMultipleDegrees)
    
def test_parse_string_or(self):
    filter_string = "maximum 3 vertices with degree 2 or "
    with self.assertRaises(pf.FilterStringError):
        pf.parse_string(filter_string)
    filter_string = "maximum 3 vertices with degree 2 or"
    with self.assertRaises(pf.FilterStringError):
        pf.parse_string(filter_string)
    filter_string = "maximum 3 vertices with degree 2 or and"
    with self.assertRaises(pf.FilterStringError):
        pf.parse_string(filter_string)
    filter_string = "maximum 3 vertices with degree 2 or and 3"
    with self.assertRaises(pf.FilterStringError):
        pf.parse_string(filter_string)