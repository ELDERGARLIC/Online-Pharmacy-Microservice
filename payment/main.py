from fastapi import FastAPI, HTTPException
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

# Define a Payment approval class that inherits from HashModel
class Payment(HashModel):
    prescription_id: str
    user_id: str
    approved: str

    class Meta:
        database = redis


# Endpoint to create a new payment approval
@app.post("/payment-approvals")
def create_payment_approval(approval: Payment):
    # Save the provided Payment approval instance to the database
    return approval.save()


# Endpoint to retrieve all payment approvals
@app.get("/payment-approvals")
def get_payment_approvals():
    # Retrieve all payment approvals
    return [format_payment_approval(pk) for pk in Payment.all_pks()]


 # Format the payment approval data as needed
def format_payment_approval(pk: str):
    approval = Payment.get(pk)

    return {
        'pk': approval.pk,
        'user_id':approval.user_id,
        'prescription_id': approval.prescription_id,
        'approved': approval.approved
    }


# Endpoint to delete a specific payment by its ID
@app.get("/payment-approvals/{approval_id}")
def get_payment_approval_id(approval_id: str):
    # Retrieve the payment instance to be deleted
    payment = Payment.get(approval_id)

    # Return the deleted Payment instance
    return payment


# Endpoint to retrieve a specific payment approvals user_id
@app.get('/payment-approvals/user/{user_id}')
def get(user_id: str):
    all_payment_approvals = [format_payment_approval(pk) for pk in Payment.all_pks()]
    user_payment_approvals = []
    for payment_approval in all_payment_approvals:
        if(payment_approval['user_id'] == user_id):
            user_payment_approvals.append(payment_approval)
    
    return user_payment_approvals


# Endpoint to delete a specific payment by its ID
@app.delete("/payment-approvals/{approval_id}")
def delete_payment_approval(approval_id: str):
    # Retrieve the Payment instance to be deleted
    payment = Payment.get(approval_id)

    # Delete the Payment instance from the database
    payment.delete(approval_id)

    # Return the deleted Payment instance
    return payment


# Endpoint to update the approval status of a payment
@app.put("/payment-approvals/{payment_id}")
def update_payment_approval(payment_id: str, approved: bool):
    # Retrieve the Payment Approval instance to be updated
    approval = Payment.get(payment_id)
    
    if not approval:
        raise HTTPException(status_code=404, detail="Payment approval not found")

    # Update the approval status
    approval.approved = approved
    approval.save()
    
    return format_payment_approval(approval)
