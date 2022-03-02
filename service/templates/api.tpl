from service.client import BaseClient

{# 类名通过class_name过滤器过滤 #}
class {{ group.name | class_name }}(BaseClient):
    def __init__(self, endpoint: str):
        super({{ group.name | class_name }}, self).__init__(endpoint)
    {% for api in group.apis %}
    def {{ api.name }}(self, data: dict) -> dict:
        """
        {{ api.description }}
        :param data: 参数{% for param in api.params %}
            {{ param.label }}: {{ param.description }}
        {% endfor %}
        :return:
        """
        path = '{{ api.path }}'
        return self.{{ api.method }}(path, json=data)
    {% endfor %}