from app.services.redis_client import redis_client

METRIC_KEY = "signals_processed"


def increment_signal_count():

    result = redis_client.incr(METRIC_KEY)

    print ("METRICS INCREMENTS:", result)


def get_signal_count():

    count = redis_client.get(METRIC_KEY)

    if count is None: 
        return 0

    return int(str(count))