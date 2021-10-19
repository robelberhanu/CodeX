from fastapi import(BackgroundTask, UploadFile, 
                        File, Form, Depends, HTTPException, status)

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import dotenv_values
from pydantic import BaseModel, EmailStr
from typing import List
from .models import User
import jwt

config_credentials = dotenv_values(".env")


conf = ConnectionConfig(
    MAIL_USERNAME = config_credentials["EMAIL"],
    MAIL_PASSWORD = config_credentials["PASS"],
    MAIL_FROM = config_credentials["EMAIL"],
    MAIL_PORT = 587,
    MAIL_SERVER = "smpt.gmail.com",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True
)

class EmailSchema(BaseModel):
    email: List[EmailStr]

async def send_email(email:EmailSchema, instance: User):
    token_data = {
        "id" : instance.id,
        "username": instance.username
    }

    token = jwt.encode(token_data, config_credentials["SECRET"])

    template = f"""
        <DOCTYPE html>
        <html>
            <head>

            </head>
            <body>
                <div style= "display: flex; align-items: center; justify-content:center; flex-direction: column">
                    <h3>Account Verification</h3>
                    <br>

                    <p>Thanks for choosing Tesseract, please click on the button below to verify your account</p>
                    <a style="margin-top:1rem; padding: 1rem; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background: #0275d8; color:white;" 
                    href="http://localhost:3000/verification/?token={token}"> Verify your email</a>
                </div>
                <p>Please kindly ignore this email if you did not register for Tesseract and nothing will happen. Thanks.</p>
            
            </body>
        
        
        </html>
    
    """