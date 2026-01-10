from sqlmodel import SQLModel , Field ,Column , String , Integer , ForeignKey , TIMESTAMP
from pydantic import EmailStr
from datetime import date , datetime
from enum import StrEnum
from sqlalchemy import CheckConstraint
from typing import Optional

class RoomStatus(StrEnum) :
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    MAINTENANCE = "maintenance"

class ReservationStatus(StrEnum):
    RESERVED = "reserved"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"

class Roles(StrEnum):
    ADMIN = "admin"
    STAFF = "staff"    


class Room(SQLModel, table=True):
    __tablename__="rooms"
    id: int | None = Field(default=None, primary_key=True)
    room_number:int
    room_type:str
    capacity:int
    price:float
    status:RoomStatus

class Guest(SQLModel, table=True):
    __tablename__="guests"
    id : int | None = Field(default=None, primary_key=True)
    name : str
    phone : int
    email : EmailStr  = Field(sa_column=Column(String, unique=True))   

class Reservation(SQLModel, table=True):
    __tablename__='reservations'   
    id : int | None = Field(default=None, primary_key=True)
    guest_id : int = Field(sa_column=Column(Integer, ForeignKey("guests.id", ondelete="CASCADE")))
    room_id: int | None = Field(sa_column=Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE")))
    check_in_date : date
    check_out_date : date
    status : ReservationStatus
    per_night_rate :float
    created_at : datetime = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True), nullable=False))
    __table_args__ = tuple(
        CheckConstraint("check_in_date < check_out_date", name="check_check_in_before_check_out")
    )


class bills(SQLModel, table=True):
    __tablename__="bills"
    id : int | None = Field(default=None, primary_key=True)
    reservation_id : int = Field(sa_column=Column(Integer, ForeignKey("reservations.id", ondelete="CASCADE")))
    total_amount : int
    paid : bool
    created_at : datetime = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True), nullable=False))

class User(SQLModel, table=True):
    __tablename__="users"
    id : int | None = Field(default=None, primary_key=True) 
    username:str = Field(unique=True)
    
    password : str
    role : Roles    

class UserCreate(SQLModel):
    username : str 
    password : str
    role : Roles
    

class UserResponse(SQLModel):
    id: int
    username:str 
    role : Roles


class Token(SQLModel):
    access_token : str
    type_bearer : str

class TokenData(SQLModel):
    id : Optional[int] = None   
    

    
