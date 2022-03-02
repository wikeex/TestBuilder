import pytest
from typing import Dict
from service.client import BaseClient
from service.{{ group.name }} import {{group.name | class_name}}
from service.data_handler import *


@pytest.fixture(scope='module')
def r() -> BaseClient:
    # 需要传入endpoint
    client = {{ group.name | class_name }}()
    return client

{% for api in group.apis%}
@pytest.mark.parametrize('case', {{ api.name }}())
def test_{{ api.name }}(r: {{ group.name | class_name }}, case: Dict):
    result = r.{{api.name}}(case['data'])
    assert result['code'] == case['$responseCode'], result['msg']
{% endfor %}