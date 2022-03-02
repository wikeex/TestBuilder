from typing import List
from utils.name import camel_to_snake
from service.api import Group, Api, ReqParam
from service.converters.base import BaseConverter
import requests


def dash_to_snake(name: str) -> str:
    return name.replace('-', '_')


class SwaggerConverter(BaseConverter):
    endpoint = None
    groups = []
    path = '/v2/api-docs?group=rest'

    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self._request_data()

    def _request_data(self):
        response = requests.get(self.endpoint + self.path)
        self.data = response.json()

    def convert(self) -> List[Group]:
        groups_dict = {}
        for tag in self.data['tags']:
            group = Group()
            group.name = dash_to_snake(tag['name'])
            group.description = tag['description']

            groups_dict[group.name] = group

        for k, v in self.data['paths'].items():
            api = Api()

            # handle path
            api.path = k
            if not k.split('/')[-1:]:
                raise Exception('Unsupported path!')
            api.name = k.split('/')[-1]
            if v.get('post') is not None:
                path_items = v.get('post')
                api.method = 'post'
            elif v.get('get') is not None:
                path_items = v.get('get')
                api.method = 'get'
            else:
                raise Exception('Unsupported method!')

            # description
            api.description = path_items['summary']

            # tags
            for tag in path_items['tags']:
                group_name = dash_to_snake(tag)
                groups_dict[group_name].apis.append(api)

            # handle request params
            if path_items.get('parameters') is None:
                continue
            req_params = []
            for parameter in path_items['parameters']:
                if parameter.get('schema') is not None:
                    req_params.extend(self._combine_params(parameter['schema']['$ref'], parameter['in']))
                else:
                    req_param = ReqParam()
                    req_param.label = parameter['name']
                    req_param.name = camel_to_snake(parameter['name'])
                    req_param.required = parameter['required']
                    req_param.description = parameter['description']
                    req_param.type = parameter['type']
                    req_param.position = parameter['in']
                    req_params.append(req_param)
            api.params = req_params
        return list(groups_dict.values())

    def _combine_params(self, ref_string: str, position: str) -> List[ReqParam]:

        definition_key = ref_string.split('/')[-1]
        swagger_param = self.data['definitions'][definition_key]

        params = []
        for param_label, param_property in swagger_param['properties'].items():
            req_param = ReqParam()
            req_param.label = param_label
            req_param.name = camel_to_snake(param_label)
            req_param.description = param_property.get('description', None)
            req_param.type = param_property.get('type', 'object')

            if param_property.get('$ref') is not None:
                req_param.children.extend(self._combine_params(param_property.get('$ref'), position))
            if param_property.get('data', {}).get('$ref') is not None:
                req_param.children.extend(self._combine_params(param_property.get('data', {}).get('$ref'), position))
            if param_label in swagger_param.get('required', []):
                req_param.required = True
            req_param.position = position
            params.append(req_param)
        return params
