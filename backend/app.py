import logging
import signal
import sys
from fastapi import FastAPI
from backend.config.settings import Settings
from backend.routes.auth_routes import router as auth_router

logger = logging.getLogger("ecommerce")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

settings = Settings()
app = FastAPI(title="E-commerce Platform Backend", version="1.0.0")

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])

def shutdown_handler(signal_received: int, frame: object) -> None:
    logger.info("Shutting down application gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

@app.on_event("startup")
async def startup_event() -> None:
    logger.info("Application startup complete")

@app.on_event("shutdown")
async def shutdown_event() -> None:
    logger.info("Application shutdown complete")