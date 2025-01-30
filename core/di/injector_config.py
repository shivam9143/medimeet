import injector

from core.redis_service import RedisService


# Dependency Injection module to configure bindings
# class RedisServiceModule(injector.Module):
#     def configure(self, binder: injector.Binder):
#         # Bind IRedisConnection to RedisConnection
#         # binder.bind(IRedisConnection, to=RedisConnection)
#         # Bind RedisService to itself
#         binder.bind(RedisService, to=RedisService)
#
#
# # Create the injector instance
# redis_injector = injector.Injector(RedisServiceModule())
