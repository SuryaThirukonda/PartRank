from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine

#models, scehmas, and crud need to be imported
import schemas
import crud
import models

#create the tables
models.Base.metadata.create_all(bind=engine)


#make fastAPI
app = FastAPI()


@app.get("/")
def read_root():
    return {"Status": "OK"}


@app.get("/health")
def health_check():
    return {"yo bhai" : "code kharro"}

@app.post("/gpus/", response_model=schemas.GPURead)
def create_gpu(gpu: schemas.GPUCreate, db: Session = Depends(get_db)):
    #pull from the crud functions
    #pass in a gpu object, and also a database session which is from get_db
    return crud.create_gpu(db=db, gpu=gpu)
    

#find one gpu in specific
@app.get("/gpus/{gpu_id}", response_model=schemas.GPURead)
def read_gpu(gpu_id: int, db: Session = Depends(get_db)):
    db_gpu = crud.get_gpu(db, gpu_id=gpu_id)
    if db_gpu is None:
        raise HTTPException(status_code=404, detail="GPU not found")
    return db_gpu

#find all gpus
@app.get("/gpus/", response_model=list[schemas.GPURead])
def read_gpus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    gpus = crud.get_gpus(db, skip=skip, limit=limit)
    return gpus

@app.delete("/gpus/{gpu_id}")
def delete_gpu(gpu_id: int, db: Session = Depends(get_db)):
    db_gpu = crud.get_gpu(db, gpu_id=gpu_id)
    if db_gpu is None:
        raise HTTPException(status_code=404, detail="GPU not found")
    crud.delete_gpu(db, gpu=db_gpu)
    return {"detail": "GPU deleted"}


@app.delete("/gpus/name/{gpu_name}")
def delete_gpu_by_name(gpu_name: str, db: Session = Depends(get_db)):
    db_gpu = crud.get_gpu_by_name(db, gpu_name=gpu_name)
    if db_gpu is None:
        raise HTTPException(status_code=404, detail="GPU not found")
    crud.delete_gpu(db, gpu=db_gpu)
    return {"detail": "GPU deleted"}


@app.delete("/gpus/")
def clear_gpus(db: Session = Depends(get_db)):
    gpus = crud.get_gpus(db)
    for gpu in gpus:
        crud.delete_gpu(db, gpu=gpu)
    return {"detail": "All GPUs deleted"}