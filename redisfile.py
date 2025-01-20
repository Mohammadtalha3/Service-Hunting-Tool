import redis




def redis_connect():

# Connect to Redis
    # redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Test connection
    try:
        r.ping()
        print("Connected to Redis!")
    except redis.ConnectionError:
        print("Failed to connect to Redis.")


redis_connect()