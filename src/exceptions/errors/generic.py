"""Generic errors"""
class EntityException(Exception):
    """Entity Exception"""
    def __init__(self, message: str):
        self.message = message


class UnauthenticatedException(Exception):
    """Unauthenticated Exception"""
    def __init__(self, message: str):
        self.message = message


class UnauthorizedException(Exception):
    """Unauthorized Exception"""
    def __init__(self, message: str):
        self.message = message
