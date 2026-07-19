from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def analyze(self, request, rule_result=None, screenshot_data_url=None)-> dict:
        """Return a dict (normalized) with analysis results."""
        raise NotImplementedError
