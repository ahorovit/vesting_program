from abc import ABC, abstractmethod
import csv

class Reader(ABC):
    """Base class for reader classes
    
    EG CsvReader, JsonReader, StreamReader
    """

    @abstractmethod
    def getNextRecord(self):
        pass


class CsvReader(Reader):
    def __init__(self, csvPath: str):
        self.csvPath = csvPath

    def getNextRecord(self):
        with open(self.csvPath, "r") as handle:
            csvReader = csv.reader(handle)
            for csvRow in csvReader:
                yield csvRow

