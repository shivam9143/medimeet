from abc import ABC, abstractmethod


class IRedisConnection(ABC):
    @abstractmethod
    def get_client(self):
        pass
