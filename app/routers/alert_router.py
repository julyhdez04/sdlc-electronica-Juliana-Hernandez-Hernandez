from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.repositories.alert_repository import AlertRepository
from app.schemas.alert_schemas import AlertOut, AlertStatusUpdate
from app.services.alert_service import AlertService

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("/", response_model=list[AlertOut])
def list_open_alerts(db: Session = Depends(get_db)):
    service = AlertService(AlertRepository(db))
    return service.list_open_alerts()


@router.patch("/{alert_id}", response_model=AlertOut)
def update_alert_status(alert_id: int, update: AlertStatusUpdate, db: Session = Depends(get_db)):
    service = AlertService(AlertRepository(db))
    try:
        return service.change_status(alert_id, update.status.value)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
