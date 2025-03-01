
from flask_async_mail import FlaskCelery, SendMail
from flask import Flask, jsonify
import os
import logging
from dotenv import load_dotenv


load_dotenv()


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' )
logger = logging.getLogger(__name__)

app = Flask(__name__)



app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"
app.config["SMTP_HOST"]=os.environ.get('SMTP_HOST')
app.config["USE_TLS"]=os.environ.get('USE_TLS')
app.config["USE_SSL"]=os.environ.get('USE_SSL')
app.config["SENDER"]=os.environ.get('SENDER')
app.config["PASSWORD"] =os.environ.get('PASSWORD')




celery = FlaskCelery()
celery.init_app(app)
mailer = SendMail(app.config.items())


@celery.task
def send_client_mail():
        mailer.send_email(
        subject="Hello, I'am FlaskCelery",
        recipient=["recipient@mail.com"],
        content="""
                    <html><body><h1>Hello User, This is FlaskCelery Library Update</h1></body></html>
                """,
        content_type="html"
    )


@app.route("/send-email", methods=["POST"])
async def send_my_email():
    try: 
        send_client_mail()
        return jsonify({"msg": "📧 Sent"})
    except Exception as e:
        logging.exception(f"❌ Failed to send email: {e}")
        return jsonify({"msg": f"❌ Failed- {e}"})
    



if __name__ =="__main__":
    app.run()