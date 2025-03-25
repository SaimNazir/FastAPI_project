from fastapi import APIRouter, Body, Response, status, HTTPException, Depends

from typing import Optional, List

from ..database import get_db
from .. import schemas, utils, oauth2




router = APIRouter(
    prefix="/posts", 
    tags=["posts"]
)




@router.get("/", response_model=List[schemas.Post])
def get_posts(db=Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10,
              skip: int = 0, 
              search: Optional[str] = None):
    
    cursor = db.cursor()

    cursor.execute("SELECT * FROM posts WHERE title LIKE %s LIMIT %s OFFSET %s", (search, limit, skip))
    posts = cursor.fetchall()

    return posts



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, current_user = Depends(oauth2.get_current_user), db=Depends(get_db)):

    # Extract the user_id from the current_user dictionary
    user_id = current_user['id'] 

    cursor = db.cursor()
    
    cursor.execute(
        """
        INSERT INTO posts (title, content, published, user_id)
        VALUES (%s, %s, %s, %s) RETURNING *;
        """,
        (post.title, 
         post.content, 
         post.published, 
         user_id)
    )
    new_post = cursor.fetchone()
    db.commit()

    return new_post





@router.get("/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, current_user: int = Depends(oauth2.get_current_user), db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (post_id,))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post



@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, current_user = Depends(oauth2.get_current_user), db=Depends(get_db)):
    # Extract user_id from current_user dictionary
    user_id = current_user['id']

    cursor = db.cursor()
    
    # First check if the post exists and belongs to the current user
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (post_id,))
    post = cursor.fetchone()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {post_id} not found")
    
    if post["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to delete this post")
    
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (post_id,))
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate, current_user: int = Depends(oauth2.get_current_user), db=Depends(get_db)):
    cursor = db.cursor()

    # Extract the user_id from the current_user dictionary
    user_id = current_user['id'] 

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (
                                                                                                            post.title, 
                                                                                                            post.content, 
                                                                                                            post.published, 
                                                                                                            str(post_id),
                                                                                                           
                                                                                                            )
                    )
    updated_post = cursor.fetchone()


    if updated_post == None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if updated_post["user_id"] != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to update this post")

    db.commit()

    return updated_post