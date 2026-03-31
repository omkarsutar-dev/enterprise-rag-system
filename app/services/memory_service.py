import redis
import json

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)


def get_chat_history(session_id):

    data = redis_client.get(session_id)

    if data:
        return json.loads(data)

    return []


def save_chat_history(session_id, history, ttl=3600):

    redis_client.setex(
        session_id,
        ttl,
        json.dumps(history)
    )


def append_message(session_id, role, content):

    history = get_chat_history(session_id)

    history.append({
        "role": role,
        "content": content
    })

    save_chat_history(session_id, history)