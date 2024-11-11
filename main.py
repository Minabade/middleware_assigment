from fastapi import FastAPI, HTTPException, status, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr   
from typing import Annotated
from time import time


app = FastAPI()



userdb =  userdb = {
    "user1": {
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "height": "5'10\"",
        "age": 30
    },
    "user2": {
        "username": "janesmith",
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "janesmith@example.com",
        "height": "5'6\"",
        "age": 28
    }
}
class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    height: str
    age: int
    

#Logger Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    log_info = { "The request took": process_time, "client_host": request.client.host, "status_code": response.status_code}
    print(log_info)
    return response

#CORS Middleware
origins = ["http://localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: Annotated[User, Body()]):
    for id, users in userdb.items():
        if id == user.username and users["email"] == user.email:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    userdb[user.username] = user.model_dump() 

    return {"message": "User created successfully"}   
