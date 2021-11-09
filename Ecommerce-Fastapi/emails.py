from typing import List

import jwt
from dotenv import dotenv_values
from fastapi import (BackgroundTasks, Depends, File, Form, HTTPException,
                     UploadFile, status)
from fastapi.responses import HTMLResponse
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import BaseModel, EmailStr

from models import User

config_credentials = dotenv_values(".env")

config = ConnectionConfig(
    MAIL_USERNAME = config_credentials["EMAIL"],
    MAIL_PASSWORD = config_credentials["PASS"],
    MAIL_FROM = config_credentials["EMAIL"],
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True
)

class EmailSchema(BaseModel):
    email: List[EmailStr]

async def send_email(email: List, instance: User):
    token_data = {
        "id": instance.id,
        "username": instance.username
    }
    token = jwt.encode(token_data, config_credentials["SECRET"], algorithm="HS256")

    template = f"""
        <html>
            <body>
            <div style="display: flex; align-items: center; justify-content: center; flex-direction: column">
                <h3>Account Verification</h3>
                <br>
                <p>Thanks for shopping with us. Please click on the button to complete the verification process</p>
                <a style="margin-top: 1rem; padding: 1rem; border-radius: 0.5rem; 
                                font-size: 1rem; text-decoration: none; background: #0275d8; color: white;" 
                                href="https://localhost:8000/verification/?token={token}" target="_blank">Verify email</a>
                <p>
                <b>Ignore if you did not register</b>
                </p>
            </div>
            </body>
        </html>
    """

    message = MessageSchema(
        subject="Ecommerce Account Verification Email",
        recipients=email, # List of recipients
        body=template, 
        subtype="html"
    )


    fm = FastMail(config)
    await fm.send_message(message=message)
