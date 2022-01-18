from abc import ABC, abstractmethod
import csv
from typing import Generator

class Reader(ABC):
    """Base class for reader classes
    
    EG CsvReader, JsonReader, StreamReader
    """

    @abstractmethod
    def getNextRecord(self) -> Generator[dict, None, None]:
        pass


class CsvReader(Reader):
    """Reads data input from csv file"""

    def __init__(self, csvPath: str, header: list):
        self.csvPath = csvPath
        self.header = header

    def getNextRecord(self) -> Generator[dict, None, None]:
        """yields csv rows as list"""

        with open(self.csvPath, "r") as handle:
            csvReader = csv.reader(handle)
            for csvRow in csvReader:
                yield {key:csvRow[idx] for idx, key in enumerate(self.header)}

