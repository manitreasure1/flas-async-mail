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
mail = FlaskCelery(app)
```

Then, configure your email settings:

```python
app.config.update(
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
    MAIL_SERVER='smtp.example.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='your-email@example.com',
    MAIL_PASSWORD='your-password'
)
```
