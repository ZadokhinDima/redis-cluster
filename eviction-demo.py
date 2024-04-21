import redis
import random

keys = []

def generate_and_store_key(index, ttl, read_count):
    ttl_string = 'no_ttl'
    
    if ttl > 0:
        ttl_string = f"ttl_{ttl}"

    key = f"{index}-{ttl_string}-{read_count}_reads"
    keys.append(key)
    return key


# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Clear all data from Redis
r.flushall()

RECORDS_COUNT = 50000

for i in range(RECORDS_COUNT):
    if random.random() <= 0.3:
        ttl = 0
    else:
        ttl = random.randint(30, 120)

    read_count = random.randint(0, 10)

    key = generate_and_store_key(i + 1, ttl, read_count)
    
    if (ttl > 0):
        r.set(key, f"val_{i + 1}", ex = 60 * ttl)
    else:
        r.set(key, f"val_{i + 1}")

    print(f"Stored record {key}")

    for _ in range(read_count):
        value = r.get(key)

for key in keys:
    value = r.get(key)
    if value is None:
        print(f"Key {key} was evicted")
            
