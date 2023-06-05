from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests, time

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
    medicine_id: str
    price: float
    service_fee: float
    total: float
    quantity: int
    status: str # pending, completed, refunded
    class Meta:
        database = redis

# Endpoint to retrieve a specific order by its primary key
@app.get('/orders/{pk}')
def get(pk: str):
    return Order.get(pk)

# Endpoint to create a new order
@app.post("/orders")
async def create(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()

    # Fetch medicine information from another microservice
    req = requests.get('http://localhost:8000/medicines/%s' % body['id'])
    medicine = req.json()

    # Create a new Order instance
    order = Order(
        medicine_id= body['id'],
        price=  medicine['price'],
        service_fee= 0.2 * medicine['price'],
        total= 1.2 * medicine['price'],
        quantity= body['quantity'],
        status= 'pending'
    )
    order.save()

    # Add a background task to mark the order as completed
    background_tasks.add_task(order_completed, order)

    return order

# Background task to mark the order as completed
def order_completed(order: Order):
    time.sleep(5) # Placeholder for further implementation
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')
