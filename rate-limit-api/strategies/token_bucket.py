import time
from database import redis_client

def token_bucket_allow(api_key, capacity, refill_rate):
    now = time.time()
    key = f"rate_limit:bucket:{api_key}"
    #Get data from redis
    bucket = redis_client.hgetall(key)
    if not bucket:
        tokens = float(capacity)
        last_refill = now   
    else:
        tokens = float(bucket['tokens'])
        last_refill = float(bucket['last_refill'])
        
        time_passed = now - last_refill
        tokens = min(float(capacity), tokens + (time_passed * refill_rate))

    if tokens >= 1:
        tokens -= 1
        #Update Redis
        redis_client.hset(key, mapping={
            "tokens": tokens,
            "last_refill": now
        })
        return True, int(tokens)
    
    return False, 0