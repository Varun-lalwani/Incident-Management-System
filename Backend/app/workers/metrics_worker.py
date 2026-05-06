import time

from app.services.metrics import (
    get_signal_count
)

print("Metrics worker started...")

previous_count = 0

while True:

    current_count = get_signal_count()

    processed_last_interval = (current_count - previous_count)

    print(
        f"Signals processed: {processed_last_interval}",
        flush=True
    )

    previous_count = current_count 

    time.sleep(10)

    # Tracks high-throughput signal processing metrics
    # Operational observability for processed signals
    # Periodically logs system processing metrics