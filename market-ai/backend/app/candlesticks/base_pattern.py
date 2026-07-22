from abc import ABC, abstractmethod

class BasePattern(ABC):

    @abstractmethod
    def detect(self, df):
        pass

    