from abc import ABC, abstractmethod
from .contract import Contract, DateField, EnumField, TextField, NumericField, ValidationError

class Writer(ABC):
    """Base class for writer classes

    EG TempWriter, MySqlWriter, CsvWriter
    TODO: Implement as interface
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


class VestingAggregator():
    """In lieu of DB layer, aggregates vesting events from input file
    TODO: implement interface
    """

    VEST_VALUE = 'VEST'
    CANCEL_VALUE = 'CANCEL'

    EVENT_KEY = 'VEST'
    DATE_KEY = 'DATE'
    EMPLOYEE_ID_KEY = 'EMPLOYEE ID'
    EMPLOYEE_NAME_KEY = 'EMPLOYEE NAME'
    AWARD_ID_KEY = 'AWARD ID'
    QUANTITY_KEY = 'QUANTITY'

    @classmethod # TODO: Use staticmethod?
    def factory(cls, filterDate: str, precision: int = 0):
        contract_ = Contract({
            cls.EVENT_KEY:EnumField(cls.EVENT_KEY, (cls.VEST_VALUE,cls.CANCEL_VALUE)),
            cls.EMPLOYEE_ID_KEY:TextField(cls.EMPLOYEE_ID_KEY).setUnique(), 
            cls.AWARD_ID_KEY:TextField(cls.AWARD_ID_KEY).setUnique(), 
            cls.EMPLOYEE_NAME_KEY:TextField(cls.EMPLOYEE_NAME_KEY),
            cls.DATE_KEY:DateField(cls.DATE_KEY),
            cls.QUANTITY_KEY:NumericField(cls.QUANTITY_KEY, precision)
        })

        return VestingAggregator(contract_, filterDate, precision)

    def __init__(self, contract: Contract, filterDate: str, precision: int):
        self.result = {}
        self.contract = contract
        self.filterDate = filterDate
        self.precision = precision

    def push(self, record: dict):
        key = self.contract.getUniqueKey(record)

        if key not in self.result:
            self.result[key] = self.getDefaultResultValue(record)

        if self.isOnOrBeforeFilterDate(record):
            self.incrementTotal(key, record)

    def getDefaultResultValue(self, record: dict) -> list:
        nameField = self.contract.getContractField(self.EMPLOYEE_NAME_KEY)
        return {
            self.EMPLOYEE_NAME_KEY:nameField.getValue(record),
            self.QUANTITY_KEY: 0 if self.precision == 0 else 0.0
         } 

    def isOnOrBeforeFilterDate(self, record: dict) -> bool:
        dateField = self.contract.getContractField(self.DATE_KEY)
        dateValue = dateField.getValue(record)
        return dateValue <= self.filterDate

    def incrementTotal(self, key: tuple, record: dict):
        eventField = self.contract.getContractField(self.EVENT_KEY)
        quantityField = self.contract.getContractField(self.QUANTITY_KEY)

        sign = -1 if eventField.getValue(record) == self.CANCEL_VALUE else 1
        magnitude = quantityField.getValue(record)

        if sign < 0 and self.result[key][self.QUANTITY_KEY] < magnitude:
            raise ValidationError('CANCEL events cannot exceed VEST events to date')

        self.result[key][self.QUANTITY_KEY] += sign*magnitude

    def getVestedTotals(self) -> list[str]:
        vestedTotals = []
        sortedKeys = sorted(self.result.keys(), key=lambda x: (x[0], x[1]))
        
        # Sort by employee ID, then by award ID
        for key in sortedKeys:
            vestedTotals.append(self.buildResultRow(key))
            # vestedTotals.append()
        return vestedTotals
    
    def buildResultRow(self, key: tuple):
        resultRow = self.result[key]
        employeeId, awardId = key
        employeeName, quantity = resultRow[self.EMPLOYEE_NAME_KEY], resultRow[self.QUANTITY_KEY]
        formattedQuantity = f'{quantity:.{self.precision}f}'
        return f'{employeeId},{employeeName},{awardId},{formattedQuantity}'