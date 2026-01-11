from fastapi import APIRouter, Depends , HTTPException , status ,Response
from .. import models, utils, database
from ..database import SessionLocal
from .. import rbac , oauth2
from sqlmodel import select
from typing import List

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

@router.get("/", response_model=List[models.UserResponse])
def get_users(db: database.SessionLocal,user: models.User = Depends(rbac.require_roles(["admin"]))):
    users = db.exec(select(models.User)).all()

    return users

@router.get("/me", response_model=models.UserResponse)
def get_current_user(current_user : models.User = Depends(oauth2.get_current_user)):
    return current_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: database.SessionLocal, id: int, current_user: models.User = Depends(rbac.require_roles(["admin"]))):
    user = db.get(models.User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} not found!")
    
    db.delete(user)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/{id}", response_model=models.UserResponse)
def get_user_by_id(id: int, db: database.SessionLocal, current_user: models.User = Depends(rbac.require_roles(["admin"]))):
    user = db.get(models.User, id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} Not found!")
    
    return user

