from abc import ABC, abstractmethod

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


class 