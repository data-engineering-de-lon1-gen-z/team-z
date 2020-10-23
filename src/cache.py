class IdCache:
    def __init__(self):
        self.cache = {}

    def get(self, key: str) -> str:
        return self.cache.get(key)

    def add(self, key: str, value: str):
        self.cache.update({key: value})


cache = IdCache()
