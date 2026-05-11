# user.py içinden artık UserLogin şemasını da dışarı aktarıyoruz
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.schemas.event import EventCreate, EventResponse