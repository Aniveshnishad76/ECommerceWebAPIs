"""Celery task"""
import logging
from celery import Celery
from src.config.env import get_settings

broker_config = get_settings()

celery_master_app = Celery(
    "tasks",
    broker=f"redis://{broker_config.redis_host}:6379/13",
    backend=f"redis://{broker_config.redis_host}:6379",
    set_as_current=True,
    include=[]
)

# Inspect all nodes.
running_client = celery_master_app.control.inspect()


def is_duplicate_task(task_name):
    """method to check task is active or not"""
    is_duplicate = False
    try:
        task_dict = running_client.active()
        if task_dict is not None:
            task_list = list(task_dict.values())[0]
            is_duplicate = True
            active_task_name = [data["name"] for data in task_list if task_list]
            if task_name in active_task_name and active_task_name.count(task_name) == 1:
                is_duplicate = False
    except Exception as ex:
        logging.error(str(ex))
        is_duplicate = False
    finally:
        return is_duplicate
