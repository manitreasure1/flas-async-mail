

import logging
from .celery_ext import FlaskCelery
from .email_service import SendMail
from .version import __version__



__all__ = ["FlaskCelery", "SendMail", "__version__"]

logging.info(f"Flask-Celery Library v{__version__} initialized.")
