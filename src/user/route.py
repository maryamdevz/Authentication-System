from fastapi import APIRouter, Depends, status
from requests import Session
from src.user.dtos import RegisterationSchema, RegistrationResponseSchema, LoginResponseSchema, LoginSchema
from src.utils.db import get_db
from src.user import controller
from src.user.models import UserModel
from src.utils.helpers import is_authenticated

user_route = APIRouter(prefix="/user")

@user_route.post("/signup", response_model=RegistrationResponseSchema, status_code=status.HTTP_201_CREATED)
def signup(body: RegisterationSchema, db: Session = Depends(get_db)):
    return controller.register_user(body, db)

@user_route.post("/login", response_model=LoginResponseSchema, status_code = status.HTTP_200_OK)
def login(body: LoginSchema, db: Session = Depends(get_db)):
    return controller.login(body, db)

@user_route.get("/your_info", response_model=RegistrationResponseSchema, status_code=status.HTTP_200_OK)
def get_user_info(user: UserModel = Depends(is_authenticated)):
    return controller.get_info(user)
