from http import HTTPStatus

from app.core.enums import ResponseCode


class CustomException(Exception):
    code = HTTPStatus.BAD_GATEWAY
    error_code = HTTPStatus.BAD_GATEWAY
    message = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, message=None):
        if message:
            self.message = message


# Root classification
class ExternalServiceException(CustomException):
    http_code: int = HTTPStatus.BAD_REQUEST
    error_code: int = ResponseCode.EXTERNAL_SERVICE_CLIENT_ERROR
    message: str = ResponseCode.EXTERNAL_SERVICE_SERVER_ERROR.message


class AuthException(CustomException):
    http_code: int = HTTPStatus.UNAUTHORIZED
    error_code: int = ResponseCode.NO_AUTHORITY
    message: str = ResponseCode.NO_AUTHORITY.message


class TokenException(CustomException):
    http_code: int = HTTPStatus.BAD_REQUEST
    error_code: int = ResponseCode.TOKEN_INVALID
    message: str = ResponseCode.TOKEN_INVALID.message


class HttpException(CustomException):
    http_code: int = HTTPStatus.BAD_REQUEST
    error_code: int = ResponseCode.BASIC_HTTP_ERROR
    message: str = ResponseCode.BASIC_HTTP_ERROR.message
