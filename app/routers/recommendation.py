from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.event import EventResponse
from app.services import recommendation as rec_service

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

# NE İŞE YARIYOR?: /recommendations/1 yazdığımızda, 1 nolu kullanıcıya özel etkinlikleri getirir.
@router.get("/{user_id}", response_model=List[EventResponse])
def get_user_recommendations(user_id: int, db: Session = Depends(get_db)):
    return rec_service.get_recommendations_for_user(db=db, user_id=user_id)