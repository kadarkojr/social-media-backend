from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from src import models, schemas, utils
from database import get_db
from typing import List, Optional
import oauth2
from sqlalchemy import func


router = APIRouter(
    prefix='/posts'
)


@router.get('', response_model=List[schemas.PostOut])
def test_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user), limit: int = 100, skip: int = 0, search: Optional[str] = ""):
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(posts)
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(results)
    posts = list (map (lambda x : x._mapping, posts))
    print(posts)
    return posts

@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.Response)
def test_gets(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/{id}')#, response_model=schemas.PostOut)
def get_person(id : int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(current_user.email)

    if not post:
        raise HTTPException(status_code = 400, detail= f"user with id {id} not found")

    print(post)
    data_dict = {'post': post[0], 'votes': post[1]}
    return data_dict


@router.delete('/{id}')
def delete_person(id : int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    '''
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(""" Select * from peops where id = %s""", (str(id),))
        existing_record = cursor.fetchone()
    '''
    post = db.query(models.Post).filter(models.Post.id == id)

    print(post.first())
    if post.first() is None:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found in list")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform action")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Response)
def update_user(id : int, updated_post:schemas.PostCreate, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    '''
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
    
        cursor.execute(""" SELECT id FROM peops WHERE id = %s""", (str(id),))
        existing_record = cursor.fetchone()
    '''
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform action")
    '''    
    cursor.execute(""" UPDATE peops SET name = %s WHERE id = %s RETURNING *""", (post.name, str(id),))
    updated_post = cursor.fetchone()
    
    conn.commit()
    '''
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
