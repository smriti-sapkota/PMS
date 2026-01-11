from jose import JWTError, jwt
from .config import settings
from datetime import datetime , timedelta
from fastapi import Depends, HTTPException , status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from .database import SessionLocal
from . import models

oauth2scheme = OAuth2PasswordBearer(tokenUrl="login")




SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRATION_TIME = settings.expiration_time

def create_token(payload:dict):
    to_encode = payload.copy()

    expire = datetime.now() + timedelta(minutes=EXPIRATION_TIME)

    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY , algorithm=ALGORITHM)
     
    return encoded_jwt

def verify_access_token(token:str , credentials_exception):

    try :

        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGORITHM])

        id : int = payload.get("user_id")

        if id is None :
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception

    return id

def get_current_user(db:SessionLocal,token = Depends(oauth2scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=" couldnot validate credentials.", headers = {'WWW-Authenticate':"Bearer"})

    payload = verify_access_token(token , credentials_exception)

    user = db.get(models.User , payload)

    return user 
       
        
