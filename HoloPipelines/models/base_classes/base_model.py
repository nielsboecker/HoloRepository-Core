from abc import ABC, abstractmethod


class Base_model(ABC):
    @abstractmethod
    def predict(self):
        pass
