# 代码生成时间: 2025-08-16 11:08:33
from bottle import route, run, request

# 定义表单数据验证器
class FormValidator:
    def __init__(self):
        self.rules = {
            'username': {'required': True, 'min_length': 3},
            'email': {'required': True, 'match': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
            'password': {'required': True, 'min_length': 6}
        }

    def validate(self, form_data):
        errors = {}
        for field, rules in self.rules.items():
            if self.rules[field].get('required', False) and not form_data.get(field):
                errors[field] = f'{field} is required.'
            elif field == 'email' and self.rules[field].get('match', None):
                pattern = self.rules[field]['match']
                if not re.match(pattern, form_data.get(field, '')):
                    errors[field] = f'{field} is invalid.'
            elif rules.get('min_length', 0) and len(form_data.get(field, '')) < rules['min_length']:
                errors[field] = f'{field} must be at least {rules[