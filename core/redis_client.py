import redis
from django.conf import settings

from core.redis_client_interfaces import IRedisConnection


class RedisConnection(IRedisConnection):
    """
    Concrete class that handles the Redis connection logic.
    """

    def __init__(self):
        self._client = None

    def get_client(self):
        """
        Establishes the Redis client connection using connection pooling.
        """
        if self._client is None:
            pool = redis.ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=0
            )
            self._client = redis.StrictRedis(connection_pool=pool, decode_responses=True)
        return self._client

