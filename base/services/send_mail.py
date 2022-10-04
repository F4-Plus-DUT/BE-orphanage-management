import os
import threading

from django.core.mail import EmailMessage

from core.settings import BLOCKED_EMAIL_DOMAINS
from dotenv import load_dotenv

load_dotenv()


class EmailThread(threading.Thread):
    def __init__(
            self,
            subject=None,
            content=None,
            email=None,
            sender=None,
            email_password=None,
            from_email=None,
            cc=None,
            bcc=None,
    ):
        self.subject = subject
        self.content = content
        self.from_email = (from_email or os.getenv('DEFAULT_FROM_EMAIL'),)
        self.sender = sender or os.getenv('EMAIL_HOST_USER')
        self.mail_password = email_password or os.getenv('EMAIL_HOST_PASSWORD')
        self.recipient_list = email
        self.cc = cc
        self.bcc = bcc
        threading.Thread.__init__(self)

    def run(self):
        email_options = dict(
            subject=self.subject,
            body=self.content,
            from_email=os.getenv('DEFAULT_FROM_EMAIL'),
            to=self.recipient_list,
            cc=self.cc,
            bcc=self.bcc,
        )
        for email in self.recipient_list:
            if email and any(email.endswith(BLOCKED_EMAIL_DOMAIN)
                             for BLOCKED_EMAIL_DOMAIN in BLOCKED_EMAIL_DOMAINS):
                raise Exception(f"Email {email} is blocked!")
        msg = EmailMessage(**email_options)
        msg.content_subtype = "html"
        msg.send()


class SendMail:
    @staticmethod
    def start(email_list, subject, content, cc=None, bcc=None):
        EmailThread(
            subject=subject, email=email_list, content=content, cc=cc, bcc=bcc
        ).start()
