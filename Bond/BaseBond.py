from abc import ABC, abstractmethod

class BondAbstract(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def set_YTM(self, ytm):
        pass

    @abstractmethod
    def set_duration(self):
        pass

    @abstractmethod
    def set_modified_duration(self):
        pass

    @abstractmethod
    def set_convexity(self):
        pass

    @abstractmethod
    def value(self, y):
        pass

if __name__ == "__main__":
    a = BondAbstract()