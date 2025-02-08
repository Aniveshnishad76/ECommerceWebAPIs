""" This Module is for the sentry """
from sentry_sdk import start_transaction
from src.config.env import BaseConfig, get_settings

config: BaseConfig = get_settings()


def sentry_wrapper(operation_name: str):
    """This is the decorator for the sentry wrapper"""

    def init_sentry_transaction():
        if config.env == "local":
            try:
                with start_transaction(op="task", name=operation_name):
                    yield
            finally:
                None
        else:
            yield

    return init_sentry_transaction
