from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from backend.service.summary_service import SummaryService
from backend.model.schema import SummaryResponse

router = APIRouter()

@router.get("/", response_model=SummaryResponse)
def get_summary():
    """Get overall Pokemon database summary"""
    try:
        service = SummaryService()
        return service.get_summary()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))