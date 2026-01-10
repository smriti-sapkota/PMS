from fastapi import APIRouter, Depends , HTTPException , status 
from .. import models, utils
from ..database import SessionLocal
from .. import rbac
from sqlmodel import select

router = APIRouter(
    prefix="/users",
    tags=["User"]
)

@router.post("/", response_model=models.UserResponse) 
def create_user(db : SessionLocal , user_data : models.UserCreate) :#, current_user : models.User = Depends(rbac.require_roles(["admin"]))) :
    user = db.exec(select(models.User).where(models.User.username == user_data.username)).first()

    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User with {user_data.username} already exits!')
    
    user_data.password = utils.hash(user_data.password)
    user = models.User(**user_data.model_dump())

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

