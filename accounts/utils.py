from rest_framework.exceptions import AuthenticationFailed, APIException


def validate_not_empty(field, field_name):
    if not field or field.strip() == '':
        raise APIException (F"o Campo {field_name} não pode estar Vazio ou zer Null")