from sqlmodel import SQLModel , Field ,Column , String , Integer , ForeignKey , TIMESTAMP , Numeric , Relationship
from pydantic import EmailStr
from datetime import date , datetime
from enum import StrEnum
from sqlalchemy import CheckConstraint
from typing import Optional
from decimal import Decimal
from typing import List 

class RoomStatus(StrEnum) :
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    MAINTENANCE = "maintenance"
    INACTIVE = "inactive"

class ReservationStatus(StrEnum):
    RESERVED = "reserved"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"

class Roles(StrEnum):
    ADMIN = "admin"
    STAFF = "staff"    

class RoomType(StrEnum):
    SINGLE = "single"
    DOUBLE = "double"                  


class Room(SQLModel, table=True):
    __tablename__="rooms"
    id: int | None = Field(default=None, primary_key=True)
    room_number:int = Field(unique=True)
    room_type:RoomType
    capacity:int
    price:Decimal = Field(sa_column=Column(Numeric(10,2)))
    status:RoomStatus
    is_active : bool | None = Field(default=True)
    reservations : List["Reservation"] = Relationship(back_populates='room')

    __table_args__ = (
        CheckConstraint("capacity > 0", name = "check_capacity_more_than_zero"),
        CheckConstraint("price > 0", name="check_price_more_than_zero")
    )

class Guest(SQLModel, table=True):
    __tablename__="guests"
    id : int | None = Field(default=None, primary_key=True)
    name : str
    phone : int
    email : EmailStr  = Field(sa_column=Column(String, unique=True))
    reservations : List["Reservation"] = Relationship(back_populates="guest")  

class Reservation(SQLModel, table=True):
    __tablename__='reservations'   
    id : int | None = Field(default=None, primary_key=True)
    guest_id : int = Field(sa_column=Column(Integer, ForeignKey("guests.id", ondelete="CASCADE")))
    room_id: int | None = Field(sa_column=Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE")))
    check_in_date : date
    check_out_date : date
    no_of_guests : int
    status : ReservationStatus
    per_night_rate : Decimal = Field(sa_column=Column(Numeric(10,2)))
    created_at : datetime = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True), nullable=False))

    guest : "Guest"= Relationship(back_populates="reservations")
    room : "Room" = Relationship(back_populates="reservations")
    bill : "Bill" = Relationship(back_populates="reservation")
    
    
    __table_args__ = (
        CheckConstraint("check_in_date < check_out_date", name="check_check_in_before_check_out"),
        CheckConstraint("per_night_rate > 0", name = "check_per_night_rate_is_not_zero"),
        CheckConstraint("no_of_guests > 0", name = "check_no_of_guests_is_not_zero")
    )


class Bill(SQLModel, table=True):
    __tablename__="bills"
    id : int | None = Field(default=None, primary_key=True)
    reservation_id : int = Field(sa_column=Column(Integer, ForeignKey("reservations.id", ondelete="CASCADE")))
    total_amount : int
    paid : bool
    created_at : datetime = Field(default_factory=datetime.utcnow, sa_column=Column(TIMESTAMP(timezone=True), nullable=False))
    reservation : "Reservation" = Relationship(back_populates="bill")

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
    token_type : str

class TokenData(SQLModel):
    id : Optional[int] = None   


class RoomCreate(SQLModel):
    room_number : int
    room_type:RoomType
    capacity:int
    price:Decimal 
    status : RoomStatus
    is_active : Optional[bool] = True

class RoomUpdate(SQLModel) :
    room_number : Optional[int] = None
    room_type: Optional[RoomType] = None
    capacity: Optional[int] = None
    price: Optional[Decimal] = None 
    status : Optional[RoomStatus] = None
    is_active : Optional[bool] = None 

class RoomStatusUpdate(SQLModel):
    status : RoomStatus     

    

    
