
#password hashing + jwt auth
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone


from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine
#import models, scehmas, and crud
import schemas
import crud
import models

from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

key = os.getenv("SECRET_KEY")
if key is None:
    raise ValueError("no key in env")

algorithm = "HS256"

#avoids error if key is None, but its alr checked above, so well just force it to be a string
secret_key: str = key


#create jwt token, validate jwt token

def create_token(user_id: str, email: str):
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes = 30)
    }

    token = jwt.encode(payload, secret_key, algorithm=algorithm)

    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithm=algorithm)

        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password

def check_password(password: str, hashed_password: bytes):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)