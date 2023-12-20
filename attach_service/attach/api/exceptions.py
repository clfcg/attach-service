from rest_framework import status
from rest_framework.exceptions import APIException


class BaseCustomException(APIException):
    detail = None
    status_code = None
    default_code = None

    def __init__(self, detail, code, custom_code):
        super().__init__(detail, code)
        self.detail = detail
        self.status_code = code
        self.default_code = custom_code


class ParameterIsRequired(BaseCustomException):
    def __init__(self, param_name):
        custom_code = "409.1"
        detail = f"Параметр {param_name} обязательный для заполнения."
        super().__init__(detail, status.HTTP_400_BAD_REQUEST, custom_code)


class ParameterDataIsRequired(BaseCustomException):
    def __init__(self, param_name):
        custom_code = "409.2"
        detail = f"Параметр {param_name} не может передаваться с пустым значеним."
        super().__init__(detail, status.HTTP_400_BAD_REQUEST, custom_code)

class InvalidDateFormatOrNone(BaseCustomException):
    def __init__(self, param_name):
        custom_code = "409.3"
        detail = f"Значение параметр {param_name} должно соответствовать формату ГГГГ-ММ-ДД."
        super().__init__(detail, status.HTTP_400_BAD_REQUEST, custom_code)

class InvalidOpToken(BaseCustomException):
    def __init__(self, param_name):
        custom_code = "409.4"
        detail = f"OpToken: {param_name} не существует."
        super().__init__(detail, status.HTTP_400_BAD_REQUEST, custom_code)

class InvalidParameters(BaseCustomException):
    def __init__(self):
        custom_code = "409.5"
        detail = "Отсутствует обязательный параметр или цепочка параметров."
        super().__init__(detail, status.HTTP_400_BAD_REQUEST, custom_code)

class PersonNotFound(BaseCustomException):
    def __init__(self):
        custom_code = "409.6"
        detail = "По заданным параметрам ни одна персона не найдена."
        super().__init__(detail, status.HTTP_400_BAD_REQUEST, custom_code)

class MoreThanOnePerson(BaseCustomException):
    def __init__(self):
        custom_code = "409.7"
        detail = "По заданным параметрам найдено больше одной персоны."
        super().__init__(detail, status.HTTP_400_BAD_REQUEST, custom_code)

class InvalidAttachMethod(BaseCustomException):
    def __init__(self):
        custom_code = "409.8"
        detail = "Значение параметра attachMethod должно быть в диапазоне от 1 до 3"
        super().__init__(detail, status.HTTP_400_BAD_REQUEST, custom_code)

class InvalidAreaType(BaseCustomException):
    def __init__(self):
        custom_code = "409.9"
        detail = "Значение параметра areaType должно быть в диапазоне от 1 до 3"
        super().__init__(detail, status.HTTP_400_BAD_REQUEST, custom_code)

class InvalidEnpLen(BaseCustomException):
    def __init__(self):
        custom_code = "409.10"
        detail = "Формат ЕНП указан неверно - должен быть XXXXXXXXXXXXXXXX и содержать только разрешенные символы - цифры"
        super().__init__(detail, status.HTTP_400_BAD_REQUEST, custom_code)

class NotActivePolis(BaseCustomException):
    def __init__(self):
        custom_code = "409.11"
        detail = "Персона не имеет активного страхового полиса на дату прикрепления"
        super().__init__(detail, status.HTTP_400_BAD_REQUEST, custom_code)

class MPIError(BaseCustomException):
    def __init__(self, mpi_code, mpi_detail):
        custom_code = mpi_code
        detail = mpi_detail
        super().__init__(detail, status.HTTP_400_BAD_REQUEST, custom_code)