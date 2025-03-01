# Flask Async Mail

`flask-async-mail` is a Flask extension that simplifies sending emails asynchronously using Celery. This library is designed to help you handle email sending as a background task, improving the performance and responsiveness of your Flask applications.

## Installation

```bash
pip install flask-async-mail
```

## Usage

First, initialize the extension in your Flask application:

```python
from flask import Flask
from flask_async_mail import FlaskCelery

app = Flask(__name__)
celery = FlaskCelery()
celery.init_app(app)
```

Then, configure your email settings:

```python
app.config.update(
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
    SMTP_HOST='smtp.example.com',
    PORT=587,
    USE_TLS=True,
    USE_SSL=False,
    SENDER='your-email@example.com',
    PASSWORD='your-password'
)
```

## using celery as decorator
```python
from flask_async_mail.email_service import SendMail

mailer = SendMail(app.config.items())

@celery.task
async def send_client_mail():
    await mailer.send_email(
        subject="Hello, I'am FlaskCelery",
        recipient=["flaskcelery@example.com"],
        content="""
                    <html>
                        <body>
                            <h1>Hello user, This is FlaskCelery Library Update</h1>
                        </body>
                    </html>
                """,
        content_type="html"
    )

```

## run command
```bash
celery -A task.celery worker --loglevel=info
```


