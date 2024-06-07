from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from ..database import get_db
from typing import Optional, List
from .. import schema, models, oauth2


router = APIRouter( tags=['Posts'])

@router.get('/posts', response_model=List[schema.PostRespnse])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip:int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get('/posts/{id}',response_model=schema.PostRespnse)
def get_post(id: int, db: Session = Depends(get_db), limit: int = 10, skip: int =0 ):
    # cursor.execute("""Select * from posts where id = %s""",(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} does not exists")
    
    return post


@router.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(new_post: schema.Post, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" Insert into posts(title, content) values (%s, %s) RETURNING * """, (new_post.title, new_post.Content))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(user_id.id)
    newpost =  models.Post(owner_id = user_id.id, **new_post.dict())
    print(newpost)
    db.add(newpost)
    db.commit()
    db.refresh(newpost)

    return newpost


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT )
def delete_post(id: int, db: Session = Depends(get_db),user_id = Depends(oauth2.get_current_user)):
    # cursor.execute(""" Delete from posts where id = %s RETURNING * """,(str(id),))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    print(post.first())
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" Post with ID {id} does not exists")
    
    if post.first().owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}", status_code=status.HTTP_201_CREATED, response_model=List[schema.PostRespnse])
def update_post(id:int, updated_post: schema.Post, db: Session = Depends(get_db), user_id = Depends(oauth2.get_current_user)):
    # new_post = dict(new_post) 
    # index = findindex(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    print(post_query)
    post = post_query.first()
    print((post.__dict__))
      
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" Post with ID {id} does not exists")
    
    if post.first().owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to updated")
    
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    return post_query.first()
