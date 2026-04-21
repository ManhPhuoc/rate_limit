import time
from database import redis_client

def sliding_window_allow(api_key, limit, window):
    now = time.time()
    key = f"rate_limit:sliding:{api_key}"
    pipe = redis_client.pipeline()  
    pipe.zadd(key, {str(now): now})
    pipe.zremrangebyscore(key, 0, now - window)
    pipe.zcard(key) 
    results = pipe.execute() 
    current_count = results[2] 
    if current_count <= limit:
        return True, int(limit - current_count)
    return False, 0
