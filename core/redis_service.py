from core.redis_client import RedisConnection


class RedisService:
    """
    Service class for common Redis operations.
    """

    def __init__(self):
        # Lazy import of RedisConnection
        self.redis_connection = RedisConnection()
        self.client = self.redis_connection.get_client()

    def exists(self, key):
        """
        Check if a key exists in Redis.
        """
        return self.redis_connection.get_client().exists(key)

    def ttl(self, key):
        """
        Get the time-to-live (TTL) for a key in Redis.
        """
        return self.redis_connection.get_client().ttl(key)

    def set(self, key, value, ex=None):
        """
        Set a value in Redis with an optional expiration time (in seconds).
        """
        return self.redis_connection.get_client().set(key, value, ex=ex)

    def get(self, key):
        """
        Get a value from Redis by key.
        """
        return self.redis_connection.get_client().get(key)

    def delete(self, key):
        """
        Delete a key from Redis.
        """
        return self.redis_connection.get_client().delete(key)

    def is_retry_allowed(self, mobile_number):
        print("is_retry_allowed --------")
        retry_key = f"otp_{mobile_number}"
        print(f"self.client {self.client}")
        if self.client.exists(retry_key):
            retry_time = self.client.ttl(retry_key)
            return False, retry_time
        return True, None

    def store_otp(self, mobile_number, otp):
        otp_key = f"otp_{mobile_number}"
        self.client.set(otp_key, otp, ex=60)  # Expire after 2 minutes

    def read_otp(self, mobile_number):
        otp_key = f"otp_{mobile_number}"
        self.client.get(otp_key)

# redis_service = RedisService()
