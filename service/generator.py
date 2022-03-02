from typing import List
from jinja2 import PackageLoader, Environment
from service.api import Api, ReqParam, Group
from service.path import PATH
from utils.name import class_name
import os

env = Environment(loader=PackageLoader('service.generator', 'templates'))  # 创建一个包加载器对象
env.filters['class_name'] = class_name


def generate_api(group: Group):
    """

    :param group:
    :return:
    """
    template = env.get_template('api.tpl')  # 获取一个模板文件
    api_file = template.render(group=group)  # 渲染
    return api_file


def generate_data_handler(apis: List[Api]):
    template = env.get_template('data_handler.tpl')  # 获取一个模板文件
    api_file = template.render(apis=apis)  # 渲染
    return api_file


def generate_test(group: Group):
    template = env.get_template('test.tpl')  # 获取一个模板文件
    test_file = template.render(group=group)  # 渲染
    return test_file


def flatten_param(req_param: ReqParam):
    if req_param.type != 'object':
        return [req_param.label]
    else:
        children_name: List[str] = []
        for child in req_param.children:
            children_name.extend(flatten_param(child))
        return [f'{req_param.label}.{child_name}' for child_name in children_name]


def generate_csv(params: List[ReqParam]):
    template = env.get_template('csv.tpl')

    flattened_params = []
    for param in params:
        flattened_params.extend(flatten_param(param))

    param_file = template.render(title=','.join(flattened_params))  # 渲染
    return param_file


def write_file(root_dir: str, groups: List[Group]):
    os.makedirs(f'{root_dir}/{PATH.ROOT}', exist_ok=True)
    with open(f'{root_dir}/{PATH.ROOT}/client.py', 'w', encoding='utf-8') as f:
        template = env.get_template('client.tpl')  # 获取一个模板文件
        f.write(template.render())
    for group in groups:
        group_dir = f'{root_dir}/{PATH.ROOT}/{group.name}'
        test_data_dir = f'{group_dir}/test_data'
        os.makedirs(group_dir, exist_ok=True)
        apis_file = generate_api(group)
        with open(f'{group_dir}/{group.name}.py', 'w', encoding='utf-8') as f:
            f.write(apis_file)

        req_data_file = generate_data_handler(group.apis)
        with open(f'{group_dir}/data_handler.py', 'w', encoding='utf-8') as f:
            f.write(req_data_file)

        tests_file = generate_test(group)
        with open(f'{group_dir}/test_{group.name}.py', 'w', encoding='utf-8') as f:
            f.write(tests_file)

        # TODO: 已生成的数据文件处理
        os.makedirs(test_data_dir, exist_ok=True)
        for api in group.apis:
            test_data_file = generate_csv(api.params)
            with open(f'{test_data_dir}/{api.name}.csv', 'w', encoding='utf-8') as f:
                f.write(test_data_file)

