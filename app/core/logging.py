import logging
from app.core.config import settings

def setup_logging():
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log")
        ]
    )
    
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("tortoise").setLevel(logging.INFO)
