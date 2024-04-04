from fastapi import FastAPI,Depends,HTTPException,status,Response
from database import SessionLocal, engine, get_db
import models
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update
from pydantic import BaseModel
from typing import Optional




app=FastAPI()

class User(BaseModel):
    Name : str
    Email :str
    Password : str
  



models.Base.metadata.create_all(bind=engine)

@app.get("/users")
async def get_post(db: Session = Depends(get_db)):
    query = db.query(models.User).all()
  
    return {"message":query}        


@app.post("/postuser",status_code=status.HTTP_201_CREATED)
async def create_user(user:User, db:Session =Depends(get_db)):
    #print(post.dict())
    new_user= models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message":new_user}


@app.get("/users/{id}")
async def get_one_user(id:int,db:Session=Depends(get_db)):
    print(id)
    query=db.query(models.User).where(models.User.id==id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail=f"user with id {id} not found")
    return {"message":query}    

@app.delete("/deluser/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int , db:Session=Depends(get_db)):
    query=db.query(models.User).filter(models.User.id==id)
    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"user with id {id} not found")
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/updateuser/{id}")
async def update_user(id:int,updated_user:User, db:Session=Depends(get_db)):
   
    user_query = db.query(models.User).filter(models.User.id == id)

    user = user_query.first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")

    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return {"message":user_query.first()}



class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.get("/items/")
async def create_item(item: Item):
    return item