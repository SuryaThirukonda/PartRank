from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./partrank.db"

engine = create_engine(
    DATABASE_URL,
    #avoids errors for sqlite specifically, not needed for other databases
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)
#you pass in this Base to your models.py file so you can create tables
Base = declarative_base()


#this function gives fastAPI a database session to work with, it will be used as a dependency in the routes that need to interact with the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()