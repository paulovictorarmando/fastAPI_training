import redis
from .settings import ENV

redis_client = redis.StrictRedis(
    host=ENV.REDIS_HOST,
    port=ENV.REDIS_PORT,
    db=0,
    decode_responses=True
)
