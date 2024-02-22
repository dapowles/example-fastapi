from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/posts", tags=['Posts'])

@router.get('/', response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), 
                current_user: models.User = Depends(oauth2.get_current_user), 
                limit: int = 10, skip: int = 0, search: Optional[str]=''):
    # SQL code
    # query = "SELECT * FROM posts;"
    # result = cur.execute(query).fetchall()
    result = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return result

@router.get('/{id}', response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), 
                current_user: models.User = Depends(oauth2.get_current_user)):
    # SQL code
    # query = """select * from posts where id = %(id)s"""
    # result = cur.execute(query,{'id':id}).fetchone()
    result = db.query(models.Post).filter(models.Post.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post {id} not found")
    return result
    
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: models.User = Depends(oauth2.get_current_user)):
    # SQL code
    # query = """INSERT INTO posts (title, content, published) 
    #             VALUES (%(title)s,%(content)s,%(published)s) returning *;"""
    # result = cur.execute(query, post.model_dump()).fetchone()
    # conn.commit() 
    new_post = models.Post(user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                current_user: models.User = Depends(oauth2.get_current_user)):
    # SQL code
    # query = """delete from posts where id=%(id)s returning *;"""
    # result = cur.execute(query, {'id':id}).fetchone()
    # conn.commit() 
    result = db.query(models.Post).filter(models.Post.id==id)

    if not result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post {id} not found") 
    
    if result.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='unauthorised action')

    result.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), 
                current_user: models.User = Depends(oauth2.get_current_user)):
    # SQL code
    # pd = post.model_dump()
    # pd['id'] = id
    # query = '''update posts
    #             set title = %(title)s, content = %(content)s, published = %(published)s
    #             where id = %(id)s returning *;
    #             '''
    # result = cur.execute(query,pd).fetchone()
    # conn.commit()
    result = db.query(models.Post).filter(models.Post.id == id)

    if not result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post {id} not found")
    
    if result.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='unauthorised action')


    result.update(post.model_dump(), synchronize_session=False)
    db.commit()
    
    return result.first()


