from app.services.redis_client import redis_client
import json

QUEUE_NAME = "signal_queue"

def enqueue_signal(signal_data):

    print("ADDING TO QUEUE:", signal_data)

    redis_client.rpush(QUEUE_NAME, json.dumps(signal_data))

    print("ADDED SUCCESSFULLY")