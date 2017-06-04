import pytest
from __init__ import InformationValidator


def test_validating():
    path = InformationValidator.receive_zip()
    validator = InformationValidator()
    validator.validate_information(path, 'Trump tweet-attacks Muslim mayor of London for being soft on terror', 10)
    assert validator.all == 10
    assert validator.fake == 2
