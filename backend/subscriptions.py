import asyncio
from ariadne import convert_kwargs_to_snake_case, SubscriptionType

from store import queues
import socket
from glob import *
import json

subscription = SubscriptionType()

@subscription.source("messages")
@convert_kwargs_to_snake_case
async def messages_source(obj, info):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((socket.gethostname(), TRIAL_PORT))
            while True:
                print('listen')
                data, server = s.recvfrom(4096)
                if data:
                    msg = json.loads(data.decode('utf-8'))
                    yield str(msg)
    except asyncio.CancelledError:
        raise

@subscription.field("messages")
@convert_kwargs_to_snake_case
async def messages_resolver(message, info):
    print(message)
    # while True:
    #     print("good")
    return message
