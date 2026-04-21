import json
from database import redis_client


def set_config(api_key: str, limit: int, window: int, strategy: str):
    config_data = {
        "limit": limit,
        "window": window,
        "strategy": strategy
    }
    key = f"config:{api_key}"
    redis_client.set(key, json.dumps(config_data))

def get_config(api_key):
    key = f"config:{api_key}"
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return {
        "limit": 5,
        "window": 60,
        "strategy": "sliding_window"
    }