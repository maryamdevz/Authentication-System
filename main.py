from fastapi import FastAPI
from src.user.route import user_route
from src.utils.db import Base, engine
from src.user.models import UserModel

Base.metadata.create_all(engine)
app = FastAPI()

app.include_router(user_route)