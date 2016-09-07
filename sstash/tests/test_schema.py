from jsonschema import validate
from jsonschema.exceptions import ValidationError
import pytest

from ..schema import OUTER_SCHEMA, INNER_SCHEMA

def test_validate_outer_success():
    """
    Test validation of basic example of outer json strucutre.
    """
    inst = {
        "hash": "12345678",
        "salt": "432523453245",
        "iterations": 3,
        "enc_blob": "abcdef123456",
    }
    return validate(inst,OUTER_SCHEMA)


def test_validate_outer_failure_invalid_type():
    """
    Test validation of invalid examples of outer json structure.
    """

    inst = {
        "hash": 15,
        "salt": "432523453245",
        "iterations": 3,
        "enc_blob": "abcdef123456",
    }
    with pytest.raises(ValidationError):
        validate(inst,OUTER_SCHEMA)

def test_validate_outer_failure_integer_out_of_bound():
    inst = {
        "hash": "12345678",
        "salt": "432523453245",
        "iterations": -5,
        "enc_blob": "abcdef123456",
    }
    with pytest.raises(ValidationError):
        validate(inst,OUTER_SCHEMA)

def test_validate_outer_failure_missing_prop():
    inst = {
        "hash": "12345678",
        "salt": "432523453245",
        "iterations": 5,
    }
    with pytest.raises(ValidationError):
        validate(inst,OUTER_SCHEMA)

def test_validate_outer_failure_unknown_property():
    inst = {
        "hash": "12345678",
        "salt": "432523453245",
        "iterations": 3,
        "enc_blob": "abcdef123456",
        "new_property": "I am a new property",
    }
    with pytest.raises(ValidationError):
        validate(inst,OUTER_SCHEMA)


def test_validate_inner_success():
    """
    An example json that passes INNER_SCHEMA
    """
    inst = {
        "n1": {
            "children": {},
            "value": "n1_value",
        },
        "n3": {
            "children": {
                "n4": {
                    "children": {},
                    "value": "n4_value",
                },
                "n5": {
                    "children": {
                        "n6": {
                            "value": "n6_value",
                            "children": {},
                        }

                    },
                    "value": "n5_value",
                }

            },
        },
        "n2": {
            "children": {},
            "value": "n2_value",
        },
    }
    return validate(inst,INNER_SCHEMA)


def test_validate_inner_failure_missing_children_prop():
    inst = {
        "n1": {
            "value": "n1_value",
        },
        "n3": {
            "children": {
                "n4": {
                    "children": {},
                    "value": "n4_value",
                },
                "n5": {
                    "children": {
                        "n6": {
                            "value": "n6_value",
                            "children": {},
                        }

                    },
                    "value": "n5_value",
                }

            },
        },
        "n2": {
            "children": {},
            "value": "n2_value",
        },
    }
    with pytest.raises(ValidationError):
        validate(inst,INNER_SCHEMA)


def test_validate_inner_failure_unknown_prop():
    inst = {
        "n1": {
            "children": {},
            "value": "n1_value",
        },
        "n3": {
            "children": {
                "n4": {
                    "children": {},
                    "value": "n4_value",
                },
                "n5": {
                    "new_prop": "I am the new prop!",
                    "children": {
                        "n6": {
                            "value": "n6_value",
                            "children": {},
                        }

                    },
                    "value": "n5_value",
                }

            },
        },
        "n2": {
            "children": {},
            "value": "n2_value",
        },
    }
    with pytest.raises(ValidationError):
        return validate(inst,INNER_SCHEMA)

