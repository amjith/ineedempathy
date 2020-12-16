from typing import Dict, Any
import logging
from pathlib import Path
from .config import settings

import emails
from emails.template import JinjaTemplate


def send_email(
    email_to: str,
    subject_template: str,
    html_template: str,
    environment: Dict[str, Any],
) -> None:
    # assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    frontend = settings.FRONTEND_HOST
    reset_link = f"{frontend}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.TOKEN_EXPIRE_HOURS,
            "reset_link": reset_link,
        },
    )


def send_new_account_email(email_to: str, username: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name}: Welcome aboard {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    frontend = settings.FRONTEND_HOST
    confirmation_link = f"http://{frontend}/confirm-account?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "valid_hours": settings.TOKEN_EXPIRE_HOURS,
            "email": email_to,
            "confirmation_link": confirmation_link,
        },
    )
