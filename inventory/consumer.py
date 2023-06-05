from main import redis, Medicine
import time

key = 'order_completed'
group = 'inventory-group'

try:
    # Create a consumer group for handling order_completed events
    redis.xgroup_create(key, group)
except:
    print('Group already exists!')

while True:
    try:
        # Read messages from the order_completed stream within the consumer group
        results = redis.xreadgroup(group, key, {key: '>'}, None)

        if results != []:
            for result in results:
                obj = result[1][0][1]
                try:
                    # Retrieve the corresponding Medicine instance based on medicine_id
                    medicine = Medicine.get(str(obj['medicine_id']))
                    
                    # Update the quantity of the medicine based on the order quantity
                    medicine.quantity = medicine.quantity - int(obj['quantity'])
                    medicine.save()
                except Exception as e:
                    print(str(e))
                    # If there's an error, add the order to the refund_order stream
                    redis.xadd('refund_order', obj, '*')

    except Exception as e:
        print(str(e))
    time.sleep(1)
