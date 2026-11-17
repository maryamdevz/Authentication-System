from datetime import datetime, timedelta, timezone
from src.user.dtos import RegisterationSchema, LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import status, HTTPException
from pwdlib import PasswordHash
from src.utils.settings import settings
import jwt

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def register_user(body: RegisterationSchema, db: Session):
    user_exists = db.query(UserModel).filter(UserModel.username == body.username).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username Already Exists"
        )

    hash_password = get_password_hash(body.password.get_secret_value())

    new_user = UserModel(
        first_name = body.first_name,
        last_name = body.last_name,
        username = body.username.lower(),
        hash_password = hash_password,
        email = body.email.lower()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login(body: LoginSchema, db: Session):
    # 1. Find user using username or email
    identifier = body.identifier.lower()

    if '@' in identifier:
        user = db.query(UserModel).filter(
            UserModel.email == identifier
        ).first()
    else:
        user = db.query(UserModel).filter(
            UserModel.username == identifier
        ).first()

    # 2. Check if user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password"
        )

    # 3. Verify password
    if not verify_password(
        body.password.get_secret_value(),
        user.hash_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username/email or password"
        )

    # 4. Generate JWT expiration time
    exp_time = datetime.now(timezone.utc) + timedelta(
        minutes=settings.EXP_TIME
    )

    # 5. Generate JWT token
    token = jwt.encode(
        {
            "_id": user.id,
            "exp": exp_time
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    # 6. Return token
    return {
        "token": token
    }


def get_info(user: UserModel):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "username": user.username,
    }

    

