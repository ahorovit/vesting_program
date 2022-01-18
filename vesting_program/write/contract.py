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
            raise ValidationError(f'Invalid {self.recordIdx} value: str value expected')


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
    """Field for processing Numeric data values"""

    def __init__(self, recordIdx: str):
        super().__init__(recordIdx)
        self.precision = 0

    def validate(self, value: str):
        # TODO: accept actual numeric values
        if not value.isnumeric():
            raise ValidationError(f'Value is not numeric: {value}')

    def postProcess(self, value):
        if self.precision == 0:
            return int(value)
        else:
            #TODO implement precision
            raise TransformationError("non-zero precision not yet supported")

    



class Contract():
    """WIP: Generic mapping/validation approach for translating raw data to ORM
    
    TODO: Complete implementation. For TempWriter, build logic into Aggregator instead
    """
    def __init__(self, fields: dict[str, Field]):
        self.fields = fields
        self.uniqueKeyFields = list(filter(lambda x: x.isUnique, self.fields.values()))

    def getUniqueKey(self, record:dict):
        """Extract tuple of unique-key values from record"""
        return tuple(field.getValue(record) for field in self.uniqueKeyFields)

    def getContractField(self, key:str) -> Field:
        """Retrieve a single Field object by key"""
        if key not in self.fields:
            raise ContractError(f'Field with key {key} not found')
        return self.fields[key]

class ValidationError(ValueError):
    pass

class TransformationError(ValueError):
    pass

class ContractError(Exception):
    pass
