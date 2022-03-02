import csv
from typing import List
from builder.utils import eval_value

{% for api in apis %}
def {{ api.name }}() -> List:
    cases = []
    with open('../testdata/data/{{ api.name }}.csv', 'r', encoding='utf-8') as f:
        rows = csv.DictReader(f)

        for row in rows:
            case = {}
            case_data = {}
            for k, v in row.items():
                case_data[k] = eval_value(v)
            # TODO: 此处需要将平铺的参数重新组装起来
            data = {
                'data': {
                    {% for param in api.params%}
                    '{{param.label}}': case_data['{{param.label}}'],
                    {% endfor %}
                }
            }

            case['data'] = data
            case['$description'] = row['$description']
            case['address'] = row['address']
            case['responseCode'] = row['responseCode']

            cases.append(case)
    return cases
{% endfor %}