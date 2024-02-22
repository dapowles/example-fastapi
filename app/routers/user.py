from typing import List
from fastapi import status, HTTPException, Depends, APIRouter

from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix='/users', tags=['Users'])

@router.get('/', response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    result = db.query(models.User).all()
    return result

@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    result = db.query(models.User).filter(models.User.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"user {id} not found")
    return result

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)

    new_user = models.User(**user.model_dump())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as error:

        raise HTTPException(status_code=status.HTTP_226_IM_USED,
                detail=f"user already exists")
    return new_user