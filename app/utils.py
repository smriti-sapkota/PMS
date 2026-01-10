from passlib.context import CryptContext
from . import models

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash(password:str):
    return pwd_context.hash(password)

def verify(plain_password , hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def calculate_total_amount(reservation: models.Reservation):
    total = (reservation.check_out_date - reservation.check_in_date).days* reservation.per_night_rate

    return total
