from abc import ABC, abstractmethod

class DataFeed(ABC):
    @abstractmethod
    def load_data(self):
        pass


    @abstractmethod
    def get_ticket(self):
        pass

    @abstractmethod
    def get_latest(self):
        pass

    
