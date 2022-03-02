import pytest

from service.converters.swagger import SwaggerConverter


@pytest.fixture(scope='module')
def swagger():
    return SwaggerConverter(endpoint='http://10.199.6.54:8099')


def test_swagger(swagger: SwaggerConverter):
    swagger_group = swagger.convert()
    print(swagger_group)