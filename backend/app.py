import logging
import signal
import sys
from fastapi import FastAPI
from backend.config.settings import Settings
from backend.routes.password_reset_routes import router as password_reset_router

logger = logging.getLogger("ecommerce")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

settings = Settings()
app = FastAPI(title="E-commerce Platform Backend", version="1.0.0")

app.include_router(password_reset_router, prefix="/api/password", tags=["Password Management"])

def shutdown_handler(signal_received: int, frame: object) -> None:
    logger.info("Gracefully shutting down backend application...")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

@app.on_event("startup")
async def startup_event() -> None:
    logger.info("Backend initialized successfully")

@app.on_event("shutdown")
async def shutdown_event() -> None:
    logger.info("Backend shutdown complete")