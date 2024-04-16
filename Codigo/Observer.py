from abc import ABC, ABCMeta, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(valor, nome):
        pass
