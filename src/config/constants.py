"""Global Constants"""
from src.config.env import get_settings

config = get_settings()
APP_CONTEXT_PATH = "/ecommerce/api"
APP_CONTEXT_PATH_v2 = "/ecommerce-internal/api"
RESPONSE_HEADERS = {
    "X-XSS-Protection": "1; mode=block",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "deny",
    "Strict-Transport-Security": "deny",
    "Content-Security-Policy": "script-src 'self'",
}

ExternalApiTIMEOUT = 25

class MasterConstants:
    """Master Constants"""
    DEFAULT_TIME_ZONE = "IST"
    DEFAULT_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
    DATETIME_FORMAT_WITHOUT_T = "%Y-%m-%d %H:%M:%S"
    DEFAULT_DATE_FORMAT = "%Y-%m-%d"


class UserStatusConstant:
    """Users status constant"""
    Active = 1
    Inactive = 0


class ProductStatusConstant:
    """Products status constant"""
    Active = 1
    Inactive = 0


class CategoriesStatusConstant:
    """Categories status constant"""
    Active = 1
    Inactive = 0


class OrderStatusConstant:
    """Orders status constant"""
    Success = 1
    Pending = 2
    Failed = 0
    Canceled = 3


class PaymentsMethodsConstant:
    """Orders status constant"""
    Cash = 1
    Paytm = 2
    PhonePay = 3
    DebitCart = 4
    CreditCart = 5
