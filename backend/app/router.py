from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List
from .database import get_session
from .models import Area, WasteLog, WasteType

router = APIRouter()

# --- AREA ENDPOINTS ---

@router.post("/areas/", response_model=Area, tags=["Areas"])
def create_area(area: Area, session: Session = Depends(get_session)):
    try:
        session.add(area)
        session.commit()
        session.refresh(area)
        return area
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating area: {str(e)}")

@router.get("/areas/", response_model=List[Area], tags=["Areas"])
def read_areas(offset: int = 0, limit: int = Query(default=100, le=100), session: Session = Depends(get_session)):
    areas = session.exec(select(Area).offset(offset).limit(limit)).all()
    return areas

@router.get("/areas/{area_id}", response_model=Area, tags=["Areas"])
def read_area(area_id: int, session: Session = Depends(get_session)):
    area = session.get(Area, area_id)
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    return area

# --- WASTE LOG ENDPOINTS ---

@router.post("/logs/", response_model=WasteLog, tags=["Logs"])
def create_log(log: WasteLog, session: Session = Depends(get_session)):
    area = session.get(Area, log.area_id)
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    
    if log.weight_kg < 0:
        raise HTTPException(status_code=400, detail="Weight cannot be negative")

    session.add(log)
    session.commit()
    session.refresh(log)
    return log

@router.get("/logs/", response_model=List[WasteLog], tags=["Logs"])
def read_logs(offset: int = 0, limit: int = Query(default=100, le=100), session: Session = Depends(get_session)):
    logs = session.exec(select(WasteLog).offset(offset).limit(limit)).all()
    return logs
