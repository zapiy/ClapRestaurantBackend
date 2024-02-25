from django.conf import settings
import logging

from asgiref.sync import sync_to_async
from firebase_admin import initialize_app as initialize_firebase_admin
from firebase_admin.credentials import Certificate
from firebase_admin import messaging


_READY = False
if settings.PRODUCTION_DATABASE:
    cert_path = str(settings.BASE_DIR / "firebase-secret.json")
    initialize_firebase_admin(Certificate(cert_path))
    _READY = True

logger = logging.getLogger("firebase")

class _FirebaseMessaging:
    
    @staticmethod
    async def send_topic_message(
        *,
        topic: str,
        type: str,
        data: dict = {}
    ):
        if not _READY: return
        try:
            data.setdefault("type", type)
            await sync_to_async(messaging.send)(
                messaging.Message(
                    topic=topic,
                    data=data
                )
            )
        except Exception as e:
            logger.exception(f"Error send topic message: {e}")
        
    @staticmethod
    async def subscribe_to_topic(
        *tokens: str,
        topic: str,
    ):
        if not _READY: return
        try:
            await sync_to_async(messaging.subscribe_to_topic)(
                tokens=list(set(tokens)),
                topic=topic
            )
        except Exception as e:
            logger.exception(f"Error subscribe topic: {e}")
    
    @staticmethod
    async def unsubscribe_from_topic(
        *tokens: str,
        topic: str,
    ):
        if not _READY: return
        try:
            await sync_to_async(messaging.unsubscribe_from_topic)(
                tokens=list(set(tokens)),
                topic=topic
            )
        except Exception as e:
            logger.exception(f"Error unsubscribe topic: {e}")

        
FirebaseMessaging = _FirebaseMessaging()
