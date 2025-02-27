

from celery import Celery
from typing import Any, Optional
from flask import Flask



class FlaskCelery:
    def __init__(self, app:Optional[Flask]=None) -> None:
        self.celery = None

        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> "FlaskCelery":
        """Initialize Celery with Flask app context."""
        self.celery = Celery(app.import_name)

        self.celery.conf.update({
            "broker_url": "redis://localhost:6379/0",
            "result_backend": "redis://localhost:6379/0",
            "task_serializer": "json",
            "result_serializer": "json",
            "timezone": "UTC",
            "enable_utc": True,
            "worker_concurrency": 4,
            "worker_prefetch_multiplier": 1,
            "worker_hijack_root_logger": True,
            "worker_log_format": "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"
        })
        
        TaskBase = self.celery.Task
        class ContextTask(TaskBase):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__( self, *args, **kwargs)
        
        self.celery = ContextTask
        return self.celery

    def __getattribute__(self, name: str) -> Any:
        if self.celery:
            return getattr(self.celery, name)
        raise AttributeError(f"'FlaskCelery' object has no attribute '{name}'")



