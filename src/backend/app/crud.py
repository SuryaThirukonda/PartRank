from sqlalchemy.orm import Session

import models
import schemas

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

def get_gpus(db: Session, skip: int = 0, limit: int = 100):
    #this gets all the gpus in the database, skip and limit are for pagination
    #offset is how many results to skip, and limit is how many results to return
    return db.query(models.GPU).offset(skip).limit(limit).all()


def get_gpu_by_name(db: Session, gpu_name: str):
    return db.query(models.GPU).filter(models.GPU.name == gpu_name).first()

def delete_gpu(db: Session, gpu: models.GPU):
    db.delete(gpu)
    db.commit()