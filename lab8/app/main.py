from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import jwt
from typing import List, Optional

from . import schemas, models, auth
from .database import get_db, engine
from .config import settings
from .limiter import RateLimiter

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
limiter = RateLimiter()


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    try:
        await limiter.check_rate_limit(request)
    except HTTPException as e:
        return e
    return await call_next(request)


@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = auth.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = auth.create_refresh_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }


@app.post("/refresh", response_model=schemas.Token)
async def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, settings.secret_key,
                             algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = auth.get_user(db, username=username)
    if user is None:
        raise credentials_exception

    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }


@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.get("/books/", response_model=List[schemas.Book])
def read_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
