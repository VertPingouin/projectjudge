def singleton(cls):
    instance = cls()
    instance.__call__ = lambda: instance
    return instance