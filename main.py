from fastapi import FastAPI
from routers import products
from routers import users
from routers import basic_auth
from routers import jwt_auth
from routers import users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth.router)
app.include_router(jwt_auth.router)
app.include_router(users_db.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
