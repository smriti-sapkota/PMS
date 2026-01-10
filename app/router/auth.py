from fastapi import APIRouter , Depends , HTTPException , status
from .. import models , utils , oauth2
from ..database import SessionLocal
from sqlmodel import select
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=models.Token)
def login(db : SessionLocal , user_data:OAuth2PasswordRequestForm = Depends()):
    user = db.exec(select(models.User).where(models.User.username == user_data.username )).first()

    if not user :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials.")
    
    if not utils.verify(user_data.password , user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials.")
    
    token = oauth2.create_token({'user_id':user.id})

    return {'access_token': token , "token_type":"bearer"}