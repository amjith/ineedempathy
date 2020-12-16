from typing import Optional, List

from sqlalchemy.orm import Session

from .models import User, Room, Story
from .schemas import RoomCreate, UserCreate, StoryCreate
from pprint import pprint


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user(db: Session, id: int) -> Optional[User]:
    return db.query(User).filter(User.id == id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_story(db: Session, room_id: int, obj_in: StoryCreate) -> Story:
    print(obj_in)
    db_obj = Story(
        room_id=room_id,
        user_id=obj_in.user_id,
        description=obj_in.description,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def create_user(db: Session, room_id: int, obj_in: UserCreate) -> User:
    db_obj = User(
        room_id=room_id,
        name=obj_in.name,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_rooms(db: Session, skip: int = 0, limit: int = 10) -> List[Room]:
    return db.query(Room).offset(skip).limit(limit).all()


def get_room(db: Session, room_id: int) -> Room:
    return db.query(Room).filter(Room.id == room_id).first()


def create_room(db: Session, room: RoomCreate) -> Room:
    db_room = Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room
