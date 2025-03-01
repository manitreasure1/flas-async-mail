from celery import Celery
from typing import Any, Optional, Dict
from flask import Flask
import logging


class FlaskCelery:
    def __init__(self, app:Optional[Flask]=None, config: Optional[Dict[str, Any]] = None) -> None:
        self.celery = None
        self.config =config or {}

        if app:
            self.init_app(app)

    def init_app(self, app: Flask) -> "FlaskCelery":
        """Initialize Celery with Flask app context."""
        try:
            print("🚀 Initializing Celery...")
            self.celery = Celery(app.import_name)
            default_config = {
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
            }
            default_config.update(self.config)
            self.celery.conf.update(default_config)
            print("✅ Celery Initialized")
            
            TaskBase = self.celery.Task
            class ContextTask(TaskBase):
                def __call__(self, *args, **kwargs):
                    with app.app_context():
                        return TaskBase.__call__( self, *args, **kwargs)
            
            self.celery.Task = ContextTask
        except Exception as e:
            logging.exception(f"❌ Failed to initialize Celery: {e}")
            raise
        return self


    def __getattribute__(self, name: str) -> Any:
        print(f"🔍 Looking for: {name}")
        
        if name in object.__getattribute__(self, '__dict__'):
            return object.__getattribute__(self, '__dict__')[name]
        
        if name in FlaskCelery.__dict__:
            return object.__getattribute__(self, name)

        celery_instance = object.__getattribute__(self, 'celery')
        if celery_instance is not None and hasattr(celery_instance, name):
            return getattr(celery_instance, name)
        
        raise AttributeError(f"👎'FlaskCelery' object has no attribute '{name}'")



