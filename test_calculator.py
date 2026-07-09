import pytest
from calculator import Calculator
@pytest.fixture
def calc():
    return Calculator()
 
def test_adds_two_numbers(calc):
    assert calc.add(2, 3) == 5
 
def test_divide_by_zero_raises(calc):
    with pytest.raises(ValueError):
        calc.divide(10, 0)
