from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

from contextlib import asynccontextmanager

from fastapi import FastAPI
from routes.health import router as health_router
from routes.analysis import router as analysis_router
from routes.history import router as history_router
from routes.execution import router as execution_router
from services.history_service import HistoryService


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    HistoryService.close()

app = FastAPI(
    title="AI Test Automation Assistant",
    version="1.1.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(analysis_router)
app.include_router(history_router)
app.include_router(execution_router,prefix="/api")  # Prefix for execution routes
