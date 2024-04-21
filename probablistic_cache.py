import redis
import random
from flask import Flask, request, jsonify

app = Flask(__name__)
redis_client = redis.Redis(host='localhost', port=6379)

TTL = 60

@app.route('/<key>', methods=['GET'])
def get_value(key):
    # Use 'key' to get data from Redis
    value = redis_client.get(key)
    ttl = redis_client.ttl(key)
    print(f"Key: {key}, Value: {value}, TTL: {ttl}")
    if ttl is not None:
            ratio = (ttl / TTL)
            if random.random() > ratio:
                redis_client.delete(key)
                recompute_cache(key, value)
                print(f"Value was recomputed for key {key}.")
                return f'Recomputed with remaining {ttl} seconds.'
    return f'No recomputation. TTL: {ttl} seconds.'

@app.route('/<key>', methods=['POST'])
def post(key):
    # Use 'key' to store data in Redis
    value = request.args.get('value')

    redis_client.set(key, value, ex=TTL)
    return 'Success'

def recompute_cache(key, value):
    redis_client.set(key, value, ex=TTL)

if __name__ == '__main__':
    app.run()