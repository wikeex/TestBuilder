from service.api import Api, ReqParam, Group
from service.generator import generate_api, generate_data_handler, generate_csv, generate_test, write_file, flatten_param


def test_generate():
    api = Api()
    api.name = 'testName'
    api.description = '这是测试描述'
    param = ReqParam()
    param.label = 'test_param'
    param.description = '测试参数'
    api.params = [param]
    api.method = 'post'
    api.path = '/test'

    group = Group()
    group.name = 'testGroup'
    group.apis = [api]

    write_file('../temp', [group])


def test_flatten_param():
    param = ReqParam()
    param.name = 'test_param'
    param.label = 'testParam'
    param.description = '测试参数'
    param.type = 'object'

    param1 = ReqParam()
    param1.type = 'string'
    param1.label = 'testParam1'
    param1.name = 'test_param1'
    param1.description = '测试参数1'

    param2 = ReqParam()
    param2.type = 'string'
    param2.label = 'testParam2'
    param2.name = 'test_param2'
    param2.description = '测试参数2'

    param3 = ReqParam()
    param3.type = 'object'
    param3.label = 'testParam3'
    param3.name = 'test_param3'
    param3.description = '测试参数3'

    param4 = ReqParam()
    param4.type = 'string'
    param4.label = 'testParam4'
    param4.name = 'test_param4'
    param4.description = '测试参数4'

    param5 = ReqParam()
    param5.type = 'string'
    param5.label = 'testParam5'
    param5.name = 'test_param5'
    param5.description = '测试参数5'

    param3.children = [param4, param5]
    param.children = [param1, param2, param3]

    api = Api()
    api.name = 'testName'
    api.description = '这是测试描述'
    api.params = [param]
    api.method = 'post'
    api.path = '/test'

    group = Group()
    group.name = 'testGroup'
    group.apis = [api]

    write_file('../temp', [group])