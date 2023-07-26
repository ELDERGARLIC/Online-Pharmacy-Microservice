from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from pydantic import BaseModel
import httpx

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


# Define a Prescription class that inherits from HashModel
class Prescription(HashModel):
    user_id: str
    medicine_list: str

    class Meta:
        database = redis

# Define a model for the request body
class Order(BaseModel):
    prescription_id: str
    user_id: str


# Endpoint to create a new prescription
@app.post("/prescriptions")
async def create_prescription(prescription: Prescription):
    # Save the provided Prescription instance to the database
    result = prescription.save()

    # Creates a new order with HTTP request to the orders microservice
    url = "http://localhost:8001/orders"
    data = {"prescription_id": prescription.pk, "user_id": prescription.user_id}  # Replace with your data
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
     
    return result


# Method to format medicine_list from string
def format_medicine_list(medicine_list: str):
    medicine_list_dict = medicine_list.split('-')
    formatted_medicine_list = {}
    for medicine in medicine_list_dict:
        medicine_dict = medicine.split(':')
        formatted_medicine_list[medicine_dict[0]] = int(medicine_dict[1])
    return formatted_medicine_list 


# Endpoint to retrieve all prescriptions
@app.get("/prescriptions")
def get_prescriptions():
    # Retrieve all prescriptions
    return [format_prescription(pk) for pk in Prescription.all_pks()]


# Endpoint to retrieve prescription by ID
@app.get("/prescriptions/{prescription_id}")
def get_prescription(prescription_id: str):
    return format_prescription(prescription_id)


# Endpoint to retrieve a specific order user_id
@app.get('/prescriptions/user/{user_id}')
def get(user_id: str):
    all_prescriptions = [format_prescription(pk) for pk in Prescription.all_pks()]
    user_prescriptions = []
    for prescription in all_prescriptions:
        if(prescription['user_id'] == user_id):
            user_prescriptions.append(prescription)
    
    return user_prescriptions


def format_prescription(pk: str):
    # Retrieve a User instance by its primary key and format the data
    prescription = Prescription.get(pk)
    # Format the prescription data as needed
    return {
        'pk': prescription.pk,
        'user_id': prescription.user_id,
        'medicine_list': format_medicine_list(prescription.medicine_list) # Convert medicine_list back to a dictionary
    }


# Endpoint to delete a specific prescription by its ID
@app.delete("/prescriptions/{prescription_id}")
def delete_prescription(prescription_id: str):
    # Retrieve the Prescription instance to be deleted
    prescription = Prescription.get(prescription_id)

    # Delete the Prescription instance from the database
    Prescription.delete(prescription_id)

    # Return the deleted Prescription instance
    return prescription
