import pytest

from utils.name import snake_to_camel, camel_to_snake


@pytest.mark.parametrize('name', ['apple', 'Apple', 'one_apple', 'RED_apple', 'one_RED_apple'])
def test_snake_to_camel(name):
    print(snake_to_camel(name))


@pytest.mark.parametrize('name', ['Apple', 'oneApple', 'OneApple', 'oneREDApple', 'oneRApple', 'apple'])
def test_camel_to_snake(name):
    print(camel_to_snake(name))