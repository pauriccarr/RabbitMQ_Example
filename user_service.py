import pika
import json

# RabbitMQ connection and channel setup
connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost')
)

channel = connection.channel()

# Declare a queue named 'user_updates'
channel.queue_declare(queue='user_updates')


# Function to simulate email update in the User Service
# and publish the event
def update_user_email(user_id, new_email):

    # Simulate updating the user in the database
    print(
        f"User {user_id} email updated to "
        f"{new_email} in User Service."
    )

    # Create an event describing the update
    event_data = {
        "user_id": user_id,
        "new_email": new_email
    }

    # Serialize event to JSON
    message = json.dumps(event_data)

    # Publish event to RabbitMQ
    channel.basic_publish(
        exchange='',
        routing_key='user_updates',
        body=message
    )

    print(f"[x] Published user update event: {event_data}")


# Example: Simulate a user email update
update_user_email(
    "user_123",
    "newemail@example.com"
)

# Close the connection
connection.close()