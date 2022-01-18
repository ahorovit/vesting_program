from abc import ABC, abstractmethod
import datetime

class Field(ABC):
    """Contract Element for validating and transforming input value"""

    @abstractmethod
    def validate(self, value):
        pass

    def postProcess(self, value):
        """Default conversion makes no change"""
        return value

    def __init__(self, recordIdx: str):
        self.recordIdx = recordIdx
        self.isUnique = False

    def getValue(self, record: dict):
        """Extract, validate, convert value"""
        res = record[self.recordIdx]
        self.validate(res)
        return self.postProcess(res)

    def setUnique(self):
        """Includes a field instance in the Unique Key for a record"""
        self.isUnique = True
        return self


class TextField(Field):
    """Field for processing Text/str data values"""
    def validate(self, value):
        if not isinstance(value, str):
            raise ValidationError("str value expected")


class EnumField(TextField):
    """TODO: Field for processing Enum data values"""

    def validate(self, value):
        pass


class DateField(Field):
    """Field for processing Date data values"""

    def __init__(self, recordIdx: str):
        super().__init__(recordIdx)
        self.format = '%Y-%m-%d'
    
    def validate(self, value):
        try:
            datetime.datetime.strptime(value, self.format)
        except ValueError:
            raise ValidationError(f'Incorrect data format, should be {self.format}')


class NumericField(Field):

    def validate(self, value):
        pass


class Contract():
    """WIP: Generic mapping/validation approach for translating raw data to ORM
    
    TODO: Complete implementation. For TempWriter, build logic into Aggregator instead
    """
    def __init__(self, fields: list[Field]):
        self.fields = fields
        self.uniqueKeyFields = list(filter(lambda x: x.isUnique, self.fields))

    def getUniqueKey(self, record:dict):
        """Extract tuple of unique-key values from record"""
        res = tuple(field.getValue(record) for field in self.uniqueKeyFields)

        return res


class ValidationError(ValueError):
    pass

class TransformationError(ValueError):
    pass