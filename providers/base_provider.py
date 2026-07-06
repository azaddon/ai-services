from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def analyze(self, request):
        pass