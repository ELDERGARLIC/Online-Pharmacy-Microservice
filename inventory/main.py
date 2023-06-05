from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

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


# Define a Medicine class that inherits from HashModel
class Medicine(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


# Endpoint to retrieve all medicines
@app.get("/medicines")
def all_medicines():
    # Retrieve all primary keys of Medicine instances and format the results
    return [format_medicine(pk) for pk in Medicine.all_pks()]


def format_medicine(pk: str):
    # Retrieve a Medicine instance by its primary key and format the data
    medicine = Medicine.get(pk)
    return {
        'id': medicine.pk,
        'name': medicine.name,
        'price': medicine.price,
        'quantity': medicine.quantity
    }


# Endpoint to create a new medicine
@app.post("/medicines")
def create_medicine(medicine: Medicine):
    # Save the provided Medicine instance to the database
    return medicine.save()


# Endpoint to retrieve a specific medicine by its primary key
@app.get("/medicines/{pk}")
def get_medicine(pk: str):
    # Retrieve a Medicine instance by its primary key
    return Medicine.get(pk)


# Endpoint to delete a specific medicine by its primary key
@app.delete("/medicines/{pk}")
def delete_medicine(pk: str):
    # Retrieve the Medicine instance to be deleted
    medicine = Medicine.get(pk)
    
    # Delete the Medicine instance from the database
    Medicine.delete(pk)
    
    # Return the deleted Medicine instance
    return medicine
