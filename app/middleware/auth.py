from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.security import verify_token
from app.services.user_service import UserService
import logging

logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):
    """Authentication middleware for protected routes"""
    
    def __init__(self, app, exclude_paths: list = None):
        super().__init__(app)
        self.exclude_paths = exclude_paths or [
            "/docs", "/redoc", "/openapi.json",
            "/api/v1/users/register", "/api/v1/users/login",
            "/health", "/info"
        ]
    
    async def dispatch(self, request: Request, call_next):
        # Check if path should be excluded
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)
        
        # Get authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        try:
            # Extract token
            token = auth_header.split(" ")[1]
            
            # Verify token
            payload = verify_token(token)
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
            
            # Get user from token
            username = payload.get("sub")
            if not username:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload"
                )
            
            # Get user from database
            user_service = UserService()
            user = await user_service.get_user_by_username(username)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )
            
            # Add user to request state
            request.state.user = user
            
            # Continue to next middleware/route
            response = await call_next(request)
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed"
            )

class AdminMiddleware(BaseHTTPMiddleware):
    """Admin-only middleware for admin routes"""
    
    async def dispatch(self, request: Request, call_next):
        # Check if user exists (set by AuthMiddleware)
        if not hasattr(request.state, 'user'):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        
        # Check if user is admin
        user = request.state.user
        if not user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        return await call_next(request)
