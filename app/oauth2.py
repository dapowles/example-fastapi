from jose import JWTError, jwt
from datetime import datetime,timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import database, schemas, models,config



oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'login')

SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expiry_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str, credentials_exeption):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        if id is None:
            raise credentials_exeption
        token_data = schemas.TokenData(id=id)
    except JWTError:
        print(JWTError.__dict__)
        raise credentials_exeption
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail='unable to authenticate', headers={'WWW-authenticate': 'Bearer'})
    
    token = verify_access_token(token, credentials_exeption)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    print('==================================================================')
    print(user)
    return user
