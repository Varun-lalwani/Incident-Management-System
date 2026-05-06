import time 
import json

from typing import cast

from app.services.redis_client import redis_client
from app.services.signal_store import (store_raw_signal)
from app.services.debounce import (process_signal)
from app.services import metrics 

QUEUE_NAME = "signal_queue"

print ("worker started. . .")

while True:

    print("Checking queue...")

    signal = redis_client.lpop(QUEUE_NAME)

    print("QUEUE RESULT:", signal)

    if signal:
        signal_str = cast(str, signal)
        
        signal_data = json.loads(signal_str)
        
        print(f"Processing: {signal_data}")
        
        store_raw_signal(signal_data)

        process_signal(signal_data["component_id"], signal_data["severity"])

        metrics.increment_signal_count()

    else:

        time.sleep(1)



