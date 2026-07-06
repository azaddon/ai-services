from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

from fastapi import FastAPI
from routes.health import router as health_router
from routes.analysis import router as analysis_router

app = FastAPI(
    title="AI Test Automation Assistant",
    version="1.0.0"
)

app.include_router(health_router)
app.include_router(analysis_router)