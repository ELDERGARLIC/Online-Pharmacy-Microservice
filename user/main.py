from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from redis_om import get_redis_connection, HashModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
import httpx
import json

# Create a FastAPI instance
app = FastAPI()

# Configure CORS middleware to allow cross-origin requests from http://localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

# Connect to Redis with the given connection details
redis = get_redis_connection(
    host="redis-15342.c293.eu-central-1-1.ec2.cloud.redislabs.com",
    port=15342,
    password="zH7QtY1d2bx9mjq7hpdYufeLRsOYXzCG",
    decode_responses=True
)

# Define a User class that inherits from HashModel
class User(HashModel):
    username: str
    name: str
    address: str
    email: str
    password: str

    class Meta:
        database = redis

# Define a Prescription class that inherits from HaseModel
class Prescription(BaseModel):
    token: str
    medicine_list: str


# Password hashing and verification
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Generate a hashed password
def get_password_hash(password: str) -> str:
    return password_context.hash(password)


# Verify a password against its hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


# JWT configuration
SECRET_KEY = "c9dc9278a6d34b64979dce9c6f4e8326"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60000

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


# Generate an access token
def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# JUST FOR DEBUGGING!
# Endpoint to retrieve all USERS
@app.get("/users")
def all_users():
    # Retrieve all primary keys of users instances and format the results
    return [format_user(pk) for pk in User.all_pks()]


def format_user(pk: str):
    # Retrieve a User instance by its primary key and format the data
    user = User.get(pk)
    return {
        'id': user.pk,
        'name': user.name,
        'username': user.username
    }


# JUST FOR ADMIN!
# Endpoint to delete a specific user by its primary key
@app.delete("/users/{pk}")
def delete_user(pk: str):
    # Retrieve the User instance to be deleted
    user = User.get(pk)
    
    # Delete the User instance from the database
    User.delete(pk)
    
    # Return the deleted User instance
    return user


# Endpoint to create a new user
@app.post("/users/signup")
def create_user(user: User):
    # Save the provided User instance to the database
    user.password = get_password_hash(user.password)
    return user.save()


# Endpoint for user login and token generation
@app.post("/users/signin")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User.get(form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Protected endpoint that requires authentication
@app.get("/users/{token}")
async def read_users_me(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    user = User.get(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# Authenticates the user based on their token
async def verify_user(token: str):
    url = f'http://127.0.0.1:8004/users/{token}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return(json.loads(response.content.decode('utf-8')))

# Create a route for the POST request
@app.post("/users/new-prescription")
async def create_prescription(prescription: Prescription):
    user_json = await verify_user(prescription.token)
    
    url = "http://localhost:8002/prescriptions"
    data = {"user_id": user_json['pk'], "medicine_list": prescription.medicine_list}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        return(json.loads(response.content.decode('utf-8')))
