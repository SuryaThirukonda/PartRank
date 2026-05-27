from sqlalchemy.orm import Session

import models
import schemas
from typing import List

#this line creates one gpu row in the database

#create
def create_gpu(db: Session, gpu: schemas.GPUCreate):
    #pass in the database session, and the gpu object from the request
    #create a new GPU object using the scehma.GPUCreate, add it to db session, and then update db with db.commit() 
    db_gpu = models.GPU(
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
    return db.query(models.GPU).filter(models.GPU.id == gpu_id).first()

def get_gpus(db: Session, skip: int = 0, limit: int = 9999, 
             Max_price: int = 9999, Sort_by_Pricetoperf_asc: bool = False, 
             Min_price: int = 0, Sort_by_Performance_desc: bool = True, search: str = "",
             Sort_by_Performance_asc: bool =  False, Sort_by_Pricetoperf_desc: bool = False,
             SortPriceAsc: bool = False, SortPriceDesc: bool = False
             ):
    #this gets all the gpus in the database, skip and limit are for pagination
    #offset is how many results to skip, and limit is how many results to return
    query = db.query(models.GPU)

    # Apply price filter
    query = query.filter(models.GPU.price <= Max_price)
    query = query.filter(models.GPU.price >= Min_price)
    if (SortPriceAsc):
        query = query.order_by(models.GPU.price.asc())
    if (SortPriceDesc):
        query = query.order_by(models.GPU.price.desc())
    if (search):
        query = query.filter(models.GPU.name.ilike(f"%{search}%"))
    
    if Sort_by_Performance_desc:
        query = query.order_by(models.GPU.performance.desc())

    if Sort_by_Performance_asc:
        query = query.order_by(models.GPU.performance.asc())

    # Apply sorting
    if Sort_by_Pricetoperf_asc:
        query = query.order_by((models.GPU.price / models.GPU.performance).asc())
    
    if Sort_by_Pricetoperf_desc:
        query = query.order_by((models.GPU.price / models.GPU.performance).desc())


    query = query.offset(skip).limit(limit)

    return query.all()


def get_gpu_by_name(db: Session, gpu_name: str):
    return db.query(models.GPU).filter(models.GPU.name == gpu_name).first()

def delete_gpu(db: Session, gpu: models.GPU):
    db.delete(gpu)
    db.commit()

def get_gpus_filtered(db: Session, performance_min: int, performance_max: int) -> List[models.GPU]:
    return (
        db.query(models.GPU)
        .filter(models.GPU.performance.between(performance_min, performance_max))
        .all()
    )

def search_gpus_by_name(db: Session, name_query: str) -> List[models.GPU]:
    return(
        db.query(models.GPU)
        .filter(models.GPU.name.ilike(f"%{name_query}%"))
        .all()
        #%% allows you to search for a string inside another string
    )

