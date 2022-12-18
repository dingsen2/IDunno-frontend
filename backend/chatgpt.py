import socket
from ariadne import make_executable_schema, load_schema_from_path, ObjectType, resolver, field, publish
from ariadne.asgi import GraphQL
from flask import Flask, request

app = Flask(__name__)

# Load the GraphQL schema from the schema file
type_defs = load_schema_from_path('schema.graphql')

# Define a GraphQL object type for the DataType class using the @ObjectType decorator
@ObjectType
class DataType:
    users: int
    online: int

# Define a GraphQL subscription type using the @ObjectType decorator
class SubscriptionType(ObjectType):
    @ObjectType
    class Subscription:
        data_changed = field(DataType)

# Map resolver functions to schema
schema = make_executable_schema(type_defs, [SubscriptionType])

# Create an instance of the Ariadne GraphQL class
graphql = GraphQL(schema)

def listen_for_socket_data():
    # Set up a socket to listen for data
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 1234))
    sock.listen(1)

    while True:
        conn, addr = sock.accept()
        data = conn.recv(1024)
        # Process the received data and update the variables
        updated_users = get_updated_users()
        updated_online = get_updated_online()
        # Trigger the GraphQL subscription by publishing an event
        publish(
            'dataChanged',
            {'users': updated_users, 'online': updated_online}
        )

# Start a new thread to listen for socket data
thread = threading.Thread(target=listen_for_socket_data)
thread.start()

if __name__ == '__main__':
    app.run()
