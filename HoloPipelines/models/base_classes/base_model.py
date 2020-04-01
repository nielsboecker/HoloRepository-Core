from abc import ABC, abstractmethod


class Base_model(ABC):
    @abstractmethod
    def predict(self, input_folder, output_folder):
        pass
