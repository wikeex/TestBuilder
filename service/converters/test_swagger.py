import pytest

from service.converters.swagger import SwaggerConverter, SwaggerYmlConverter


@pytest.fixture(scope='module')
def swagger():
    return SwaggerConverter(endpoint='http://10.199.6.54:8099')


@pytest.fixture(scope='module')
def swagger_yml():
    return SwaggerYmlConverter('swagger.yml')


def test_swagger(swagger: SwaggerConverter):
    swagger_group = swagger.convert()
    print(swagger_group)


def test_swagger_yml(swagger_yml):
    swagger_group = swagger_yml.convert()
    print(swagger_group)