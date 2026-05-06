from app.services.mongo_client import signals_collection 

def store_raw_signal(signal_data):

    result = signals_collection.insert_one(signal_data)

    return str(result.inserted_id)