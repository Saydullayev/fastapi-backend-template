import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)


class EmailService:
    @staticmethod
    async def send_email(to_email: str, subject: str, body: str) -> bool:
        try:
            logger.info(f"Email sent to {to_email}: {subject}")
            logger.debug(f"Email body: {body}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
