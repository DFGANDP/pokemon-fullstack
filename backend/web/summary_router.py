from fastapi import APIRouter, HTTPException

from backend.model.schema import SummaryResponse
from backend.service.summary_service import SummaryService

router = APIRouter()


@router.get("/", response_model=SummaryResponse)
def get_summary():
    """Get overall Pokemon database summary"""
    try:
        service = SummaryService()
        return service.get_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
