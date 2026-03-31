import redis
import json

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0)
# redis_client = redis.Redis(host="redis", port=6379, db=0)


def generate_cache_key(tenant_id, query, filters):

    key = f"{tenant_id}:{query}"

    if filters:
        for k, v in filters.items():
            if v:
                key += f":{k}={v}"

    return key


def get_cached_response(key):

    data = redis_client.get(key)

    if data:
        return json.loads(data)

    return None


def set_cached_response(key, value, ttl=3600):

    redis_client.setex(
        key,
        ttl,
        json.dumps(value)
    )