from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time
import logging

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Logging middleware for all requests and responses"""
    
    async def dispatch(self, request: Request, call_next):
        # Start time
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")
        logger.debug(f"Headers: {dict(request.headers)}")
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            logger.info(f"Response: {response.status_code} - {duration:.3f}s")
            
            return response
            
        except Exception as e:
            # Calculate duration
            duration = time.time() - start_time
            
            # Log error
            logger.error(f"Error: {str(e)} - {duration:.3f}s")
            raise
