from fastapi import APIRouter
from services.execution_service import run_tests

router = APIRouter()

@router.post("/run-tests")
def execute():
    return run_tests()