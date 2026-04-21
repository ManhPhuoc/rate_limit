import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
try:
    if redis_client.ping():
        print("Redis connection successful")
except Exception as e:
    print(f"Error connecting to Redis: {e}")