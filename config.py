import redis
class Config(object):
    # config info
    SECRET_KEY = "lx*lx"
    SESSION_TYPE='filesystem'

    #db
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:666888@127.0.0.1:3306/blog_lx"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

     #redis
    REDIS_HOST="127.0.0.1"
    REDIS_PORT= 6379

    #session_redis
    SESSION_TYPE = "redis"
    REDIS_HOST_S = "127.0.0.1"
    REDIS_PORT_S = 6379
    SESSION_REDIS=redis.StrictRedis(host=REDIS_HOST_S,port=REDIS_PORT_S)
    SESSION_USE_SIGNER=True
    PERMANENT_SESSION_LIFETIME=86400

class DevelopmentConfig(Config):
    DEBUG = True




class ProductConfig(Config):
    pass

config_map={
    "develop":DevelopmentConfig,
    "product":ProductConfig
}