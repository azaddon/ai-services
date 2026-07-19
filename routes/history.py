from fastapi import APIRouter, HTTPException, Query, status

from services.history_service import HistoryService, HistoryUnavailableError

router = APIRouter(prefix="/api/v1/history", tags=["history"])


def unavailable(exc: Exception):
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Failure history is unavailable",
    ) from exc


@router.get("/failures")
def list_failures(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=25, ge=1, le=100),
):
    try:
        return HistoryService.list(skip, limit)
    except HistoryUnavailableError as exc:
        unavailable(exc)
    except Exception as exc:
        unavailable(exc)


@router.get("/analytics")
def analytics():
    try:
        return HistoryService.analytics()
    except HistoryUnavailableError as exc:
        unavailable(exc)
    except Exception as exc:
        unavailable(exc)
