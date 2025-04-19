from app.calculation import add
import pytest


@pytest.mark.parametrize("num1, num2, expected", [
    (1, 2, 3),
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),]
    )
def test_add(num1, num2, expected):

    result = add(num1, num2)
    assert result == expected