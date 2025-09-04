from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.db import init_db, close_db
from app.core.logging import setup_logging
from app.api.v1 import users, products, orders
from app.middleware.auth import AuthMiddleware, AdminMiddleware
from app.middleware.logging import LoggingMiddleware
from app.middleware.rate_limit import RateLimitMiddleware

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting up application...")
    await init_db()
    logger.info("Database initialized")

    yield

    # Shutdown
    logger.info("Shutting down application...")
    await close_db()
    logger.info("Database connections closed")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FastAPI project with Tortoise ORM - Users, Products, and Orders management",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middlewares
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=100)
app.add_middleware(AuthMiddleware)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Server sizga xizmat ko'rsatishdan bosh tortdi"}
    )


app.include_router(users.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": settings.app_name}


@app.get("/info") # productionga chiqarish payti o'chirib qo'yishni tavsiya qilaman
async def info():
    """Application information"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
        "database_url": settings.database_url.split("://")[0] + "://***"
    }