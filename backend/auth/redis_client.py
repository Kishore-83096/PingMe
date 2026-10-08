import redis

from config import REDIS_URL


def check_redis_connection():
    """
    Checks whether PingMe can successfully connect to Redis/Valkey.

    PING is used because we only need to verify the Redis connection
    at this stage.
    """
    try:
        client = redis.from_url(
            REDIS_URL,
            socket_connect_timeout=5,
            socket_timeout=5,
        )

        return client.ping()

    except redis.RedisError:
        return False