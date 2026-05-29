import bcrypt
from sqlalchemy.orm import Session

import app.models
import app.schemas
from typing import List
from app.auth import hash_password, create_token, verify_token, check_password
#this line creates one gpu row in the database

#create
def create_gpu(db: Session, gpu: app.schemas.GPUCreate):
    #pass in the database session, and the gpu object from the request
    #create a new GPU object using the scehma.GPUCreate, add it to db session, and then update db with db.commit() 
    db_gpu = app.models.GPU(
        name = gpu.name, 
        price = gpu.price,
        performance = gpu.performance
    )
    db.add(db_gpu)
    db.commit()

    #reload the object so it includes all the auto generated fields like id and created_at
    db.refresh(db_gpu)

    return db_gpu 
    #returns the new created gpu object, which will be converted to JSON and sent back to the client by FastAPI

#read
def get_gpu(db: Session, gpu_id : int):
    #models.GPU is the SQLAlchemy model, and query() is how you query the database for that model, filter() is how you filter the results, and first() gets the first result
    return db.query(app.models.GPU).filter(app.models.GPU.id == gpu_id).first()

def get_gpus(db: Session, skip: int = 0, limit: int = 9999, 
             Max_price: int = 9999,Min_price: int = 0, Sort_by: str = "performance", search: str = "",
             sort_as: str = "asc"
             ):
    #this gets all the gpus in the database, skip and limit are for pagination
    #offset is how many results to skip, and limit is how many results to return
    query = db.query(app.models.GPU)

    # Apply price filter
    query = query.filter(app.models.GPU.price <= Max_price)
    query = query.filter(app.models.GPU.price >= Min_price)

    if (Sort_by == "price" and sort_as == "asc"):
        query = query.order_by(app.models.GPU.price.asc())
    if (Sort_by == "price" and sort_as == "desc"):
        query = query.order_by(app.models.GPU.price.desc())
    if (search):
        query = query.filter(app.models.GPU.name.ilike(f"%{search}%"))
    
    if (Sort_by == "performance" and sort_as == "desc"):
        query = query.order_by(app.models.GPU.performance.desc())

    if (Sort_by == "performance" and sort_as == "asc"):
        query = query.order_by(app.models.GPU.performance.asc())

    # Apply sorting
    if (Sort_by == "price_to_performance" and sort_as == "asc"):
        query = query.order_by((app.models.GPU.price / app.models.GPU.performance).asc())
    
    if (Sort_by == "price_to_performance" and sort_as == "desc"):
        query = query.order_by((app.models.GPU.price / app.models.GPU.performance).desc())


    query = query.offset(skip).limit(limit)

    return query.all()


def get_gpu_by_name(db: Session, gpu_name: str):
    return db.query(app.models.GPU).filter(app.models.GPU.name == gpu_name).first()

def delete_gpu(db: Session, gpu: app.models.GPU):
    db.delete(gpu)
    db.commit()

def get_gpus_filtered(db: Session, performance_min: int, performance_max: int) -> List[app.models.GPU]:
    return (
        db.query(app.models.GPU)
        .filter(app.models.GPU.performance.between(performance_min, performance_max))
        .all()
    )

def search_gpus_by_name(db: Session, name_query: str) -> List[app.models.GPU]:
    return(
        db.query(app.models.GPU)
        .filter(app.models.GPU.name.ilike(f"%{name_query}%"))
        .all()
        #%% allows you to search for a string inside another string
    )

#__________________________________________________Users___________________________________________________________
#__________________________________________________________________________________________________________________

def create_user(db: Session, user: app.schemas.UserBase, password: str, email :str = ""):
    db_user = app.models.User(
        name = user.name,
        hashed_password = hash_password(password),
        email = email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

import jwt

def login_user(db : Session, name: str, email: str, password: str):
    if email:
        db_user = db.query(app.models.User).filter(app.models.User.email == email).first()
    else:
        db_user = db.query(app.models.User).filter(app.models.User.name == name).first()

    if not db_user:
        return None
    
    if not check_password(password, db_user.hashed_password):
        return None
    return create_token(db_user.id, db_user.email)
    #return db_user


def get_user(db: Session, name_query: str) -> List[app.models.User]:
    return(
        db.query(app.models.User).
        filter(app.models.User.name == name_query)
        .all()
    )