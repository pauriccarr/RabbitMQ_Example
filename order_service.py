import pika
import json

# RabbitMQ connection and channel setup
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)
channel = connection.channel()

# Declare the same queue to listen for events
channel.queue_declare(queue='user_updates')


# Function to simulate updating the user's email
# in the Order Service's database
def update_email_in_order_service(user_id, new_email):
    print(
        f"Updating email for user {user_id} "
        f"in Order Service to {new_email}"
    )


# Callback function to process messages from RabbitMQ
def callback(ch, method, properties, body):
    event_data = json.loads(body)

    print(f"[x] Received user update event: {event_data}")

    # Update email in the Order Service's database
    update_email_in_order_service(
        event_data['user_id'],
        event_data['new_email']
    )


# Setup the consumer to listen to 'user_updates' queue
channel.basic_consume(
    queue='user_updates',
    on_message_callback=callback,
    auto_ack=True
)

print(
    "[*] Waiting for messages from User Service. "
    "To exit, press CTRL+C"
)

channel.start_consuming()