# flask-async-mail
A Flask extension for sending emails asynchronously using Celery. **flask-async-mail** simplifies email workflow management, eliminates explicit object importing overhead, and provides fine-grained control over execution and retry mechanisms.

## Features
- **Simplified Extension Setup:** Direct integration via FlaskCelery without requiring explicit import of standard Mail objects.

- **Flexible Celery Binding:** Automatically attaches to the active Celery instance or creates a dedicated background object if none is explicitly provided.

- **Dual Execution Paradigms:** High-level convenience methods alongside explicit `BaseMailTask` subclassing for advanced job control.

- **No Lost Controls:** Retain full access to native Celery features (`autoretry_for`, `queues`, `backoff strategies`) via standard Python class inheritance (`BaseMailTask`).

- **Native Async & Sync Support:** Out-of-the-box support for synchronous dispatch and coroutines (`send_async`, `send_template_async`).

- **Template Rendering:** Direct template rendering supporting flexible context payloads (`Any`) and `content-type` control.

- **Dynamic Override System:** Override default SMTP parameters (`host`, `port`, `auth`, `timeouts`) directly at invocation time.

- **Full Celery Passthrough:** Complete access to Celery directives (`max_retries`, `countdown`, `retry_backoff`, `queue`).

- **Backward Compatibility:** Preserves legacy `SendMail` class support.

```bash
pip install flask-async-mail
```
## Quickstart
Initialize `FlaskCelery` with your Flask application configuration. If an existing Celery app is not explicitly attached, FlaskCelery will automatically bind to the active Celery app context or create an instance on the fly.

```py
from flask import Flask
from flask_async_mail import FlaskCelery

app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL="redis://localhost:6379/0",
    CELERY_RESULT_BACKEND="redis://localhost:6379/0",
    SMTP_HOST="smtp.example.com",
    PORT=587,
    SENDER="your-email@example.com",
    PASSWORD="your-password",
    TIMEOUT=30
)

mail = FlaskCelery()
# Celery can be explicitly passed; otherwise, the current Celery app or a fallback object is created automatically
mail.init_app(app)

@app.post("/auth/signup")
def signup():
    # Sign up logic...

    mail.send(
        recipients="example@mail.com",
        content="Hello from FlaskCelery",
        subject="Greetings",
        # Optional config overrides
        hostname="smtp.example.com",
        port=465,
        password="*********",
        timeout=30,
        # Celery execution directives
        max_retries=5,
        countdown=60,
        retry_backoff=True,
        queue="high_priority"
    )
    return {"status": "Email queued"}, 200
```

## Usage & API Reference
1. **Simple Email Dispatch (send / send_async):**
    Dispatches an asynchronous or coroutine-based email using default or inline overridden parameters.
    ```py
    # Synchronous / Celery Task Dispatch
    mail.send(
        recipients="user@example.com",
        subject="Welcome",
        content="Hello World"
    )

    # Coroutine Execution
    await mail.send_async(
        recipients="user@example.com",
        subject="Welcome",
        content="Hello World"
    )
    ```

2. **Template Email Dispatch (send_template / send_template_async):** Renders HTML or plain-text templates with context parameters of any format or dictionary layout.

    ```py
    mail.send_template(
        recipients=["user@example.com"],
        subject="Account Verification",
        template_name="emails/verify.html",
        context={"username": "Alex", "link": "https://example.com/verify"},
        content_type="html"
    )
    ```
    ## Parameter Reference (`send_template` & `send_template_async`)

    |Parameter|Type|Default|Description|
    |---------|------|----|----|
    |recipients|	`list[str] or str`| Required	|Recipient email address(es).|
    |subject | str|	Required|	Email subject line.|
    |template_name | str | Required | Path to the template file.|
    |context |Any|	Required	|Context payload passed directly to the template renderer.|
    |content_type | Literal["html", "plain"]| "plain"|	MIME subtype of the email message.|
    |username	|str or None|	None|	Override SMTP authentication username.|
    |hostname|	str or None |	None	|Override SMTP server hostname.|
    |port|	Literal[465, 587] | None|	None|	Override SMTP port.|
    |password|	str or None|	None|	Override SMTP authentication password.|
    |timeout|	float or None|	None|	Override SMTP socket connection timeout.|
    |max_retries|	int or None|	None|	Celery max retry limit.|
    |countdown|	int or None	|None	|Celery task execution delay |in seconds.|
    |retry_backoff|	bool or None|	None	|Enable Celery exponential retry backoff.|
    |queue|	str or None|	None	|Target Celery execution queue.|

3. **Advanced Task Configuration (`BaseMailTask`)**
**No Lost Controls:** For production applications requiring explicit error policies, subclassing `BaseMailTask` guarantees you retain full access to native Celery features (`autoretry_for`, custom `routing queues`, exponential `backoff` strategies, and `dead-letter` handling) without abstraction leaks or framework limitations.

    ```py
    from smtplib import SMTPException
    from flask_async_mail.task import BaseMailTask

    class AppMailTask(BaseMailTask):
        autoretry_for = (SMTPException, ConnectionError, TimeoutError)
        retry_kwargs = {'max_retries': 5}
        retry_backoff = True
        retry_backoff_max = 60
        queue = 'priority_emails'

    @mail.task(base=AppMailTask, bind=True)
    def send_receipt(self, recipient, receipt_data):
        formatted_body = render_receipt(receipt_data)
        self.send(
            subject="Your Purchase Receipt",
            recipient=recipient,
            content=formatted_body
        )

    @app.post("/receipt")
    def receipt():
        send_receipt.delay("user@example.com", {"item": "Book", "price": "$10"})
        return {"status": "Receipt queued"}
    ```
## Backward Compatibility
The legacy `SendMail` object remains available for existing codebases requiring direct tuple-based app configuration binding.

```py
from flask_async_mail.email_service import SendMail

mailer = SendMail(app.config.items())
```