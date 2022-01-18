from abc import ABC, abstractmethod
from contract import Contract

class Writer(ABC):
    """Base class for writer classes

    EG TempWriter, MySqlWriter, CsvWriter
    """

    @abstractmethod
    def pushRecord(self, record: dict):
        pass

class TempWriter(Writer):
    """Non-persistent implementation of Writer

    Validates/filters/Aggregates input values based on a Contract. Does not
    persist results to DB, but rather to an Aggregator object
    """

    def __init__(self):
        pass

    def pushRecord(self, record: dict):
        pass


class Aggregator():
    def __init__(self, contract: Contract, filterDate: ):
        self.result = {}
        self.contract = contract

    def push(self, record: dict):
        key = self.contract.getUniqueKey()

        if key not in self.result:
            self.contract[key] = 0 #TODO: truncate/fill
        

        
