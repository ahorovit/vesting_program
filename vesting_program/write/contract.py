from abc import ABC, abstractmethod
from typing import list

class Field(ABC):
    """Contract Element for validating and transforming input value"""

    @abstractmethod
    def validate(self, value):
        pass

    def __init__(self, recordIdx: str):
        self.recordIdx = recordIdx
        self.isUnique = False

    def getValue(self, record: dict):
        return self.validate(record[self.recordIdx])

    def setUnique(self):
        """Includes a field instance in the Unique Key for a record"""
        self.isUnique = True

class EnumField(Field):
    """Field for processing Enum data values"""

    def validate(self, value):
        pass


class DateField(Field):
    """Field for processing Date data values"""
    
    def validate(self, value):
        pass


class NumericField(Field):

    def validate(self, value):
        pass


class Contract():
    """WIP: Generic mapping/validation approach for translating raw data to ORM
    
    TODO: Complete implementation. For TempWriter, build logic into Aggregator instead
    """
    def __init__(self, fields: list[Field]):
        self.fields = fields