class RedisClient(object):
    def __init__(self, url='redis://@localhost:6379/0'):
        self.redis = redis.from_url(url=url)

    # 保证单例，减少连接数
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__instance'):
            cls.__instance = object.__new__(cls)
        return cls.__instance



if __name__ == '__main__':
    redis = RedisClient()

