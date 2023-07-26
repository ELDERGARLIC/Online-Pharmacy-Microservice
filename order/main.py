from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests, time
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

# Define an Order class that inherits from HashModel
class Order(HashModel):
    prescription_id: str
    user_id: str
    price: float
    service_fee: float
    total: float
    status: str # pending, completed, refunded
    
    class Meta:
        database = redis


# Endpoint to retrieve a specific order by its primary key
@app.get('/orders')
def get_orders():
    # Retrieve all primary keys of orders instances and format the results
    return [format_order(pk) for pk in Order.all_pks()]


# Endpoint to retrieve a specific order by its primary key
@app.get('/orders/{pk}')
def get(pk: str):
    return Order.get(pk)


# Endpoint to retrieve a specific order user_id
@app.get('/orders/user/{user_id}')
def get(user_id: str):
    all_orders = [format_order(pk) for pk in Order.all_pks()]
    user_orders = []
    for order in all_orders:
        if(order['user_id'] == user_id):
            user_orders.append(order)
    
    return user_orders


# Fromat the order for the GET requests
def format_order(pk: str):
    # Retrieve a User instance by its primary key and format the data
    order = Order.get(pk)
    return {
        'pk': order.pk,
        'user_id': order.user_id,
        'prescription_id': order.prescription_id,
        'price': order.price,
        'service_fee': order.service_fee,
        'total': order.total,
        'status': order.status
    }


# Endpoint to delete a specific order by its ID
@app.delete("/orders/{order_id}")
def delete_order(order_id: str):
    # Retrieve the Order instance to be deleted
    order = Order.get(order_id)

    # Delete the Order instance from the database
    Order.delete(order_id)

    # Return the deleted Order instance
    return order


# Endpoint to create a new order
@app.post("/orders")
async def create(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    
    # Fetch prescription information from another microservice
    req = requests.get('http://localhost:8002/prescriptions/%s' % body['prescription_id'])
    prescription = req.json()

    # Variables
    price = 0
    service_fee = 1.2

    # Adding up the total price
    for medicine,quantity in prescription['medicine_list'].items():
        url = f'http://127.0.0.1:8000/medicines/{medicine}'
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            medicine_json = json.loads(response.content.decode('utf-8'))
            price += medicine_json['price'] * quantity
    
    # Create a new Order instance
    order = Order(
        prescription_id= body['prescription_id'],
        user_id = body['user_id'],
        price=  price,
        service_fee= service_fee,
        total= service_fee * price,
        status= 'pending'
    )
    order.save()

    # Add a background task to mark the order as completed
    background_tasks.add_task(order_completed, order)

    return order


# Background task to mark the order as completed
def order_completed(order: Order):
    time.sleep(5) # Placeholder for further implementation of the payment

    # Mockup payment implementation
    url = 'http://127.0.0.1:8003/payment-approvals' 
    data = {'prescription_id': order.prescription_id, 'user_id': order.user_id, 'approved': str(True)}  

    # Confirms the payment
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print('Payment approved successful')
    else:
        print('Failed to send the POST request:', response.text)

    # Set the order's status to completed after verifying the payment
    order.status = 'completed'
    order.save()

    # Fetch prescription information from another microservice
    url = 'http://127.0.0.1:8000/medicines' 
    data = {'prescription_id': order.prescription_id}  

    # Updates the inventory
    response = requests.put(url, json=data)
    if response.status_code == 200:
        print('PUT request successful')
    else:
        print('Failed to send the PUT request:', response.text)

    

