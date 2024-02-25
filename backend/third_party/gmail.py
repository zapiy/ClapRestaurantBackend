from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, Tuple
from jinja2 import Template
import aiosmtplib, asyncio

from django.conf import settings

GMAIL_CREDS: Tuple[str, str] = settings.GMAIL_CREDS
GMAIL_HOST = 'smtp.gmail.com'
GMAIL_PORT = 587


class _GmailSender:
    def __init__(self) -> None:
        if not GMAIL_CREDS: return
        self._lock = asyncio.Lock()
        self._sender = GMAIL_CREDS[0]
        self._cached_templates: Dict[str, Template] = {}
    
    async def send_mail(
        self,
        *,
        recipient: str,
        text: str,
        title: str = None,
    ):
        if not GMAIL_CREDS or recipient == GMAIL_CREDS[0]: return
        try:
            async with self._lock:
                async with aiosmtplib.SMTP(
                    hostname=GMAIL_HOST,
                    port=GMAIL_PORT,
                    username=GMAIL_CREDS[0],
                    password=GMAIL_CREDS[1]
                ) as smtp:
                    msg = MIMEMultipart('alternatives')
                    msg['From'] = self._sender
                    msg['To'] = recipient
                    if title:
                        msg['Subject'] = title
                    
                    msg.attach(MIMEText(str(text), 'plain'))

                    await smtp.sendmail(self._sender, recipient, msg.as_string())
            
            return True
        except:
            pass
        return False
    
    
GmailSender = _GmailSender()
