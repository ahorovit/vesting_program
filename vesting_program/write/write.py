from abc import ABC, abstractmethod
from .contract import Contract, DateField, TextField, NumericField

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


class VestingAggregator():
    """In lieu of DB layer, aggregates vesting events from input file"""

    EVENT_KEY = 'VEST'
    DATE_KEY = 'DATE'
    EMPLOYEE_ID_KEY = 'EMPLOYEE ID'
    EMPLOYEE_NAME_KEY = 'EMPLOYEE NAME'
    AWARD_ID_KEY = 'AWARD ID'
    QUANTITY_KEY = 'QUANTITY'

    @classmethod
    def factory(cls, filterDate):
        contract_ = Contract({
            cls.EMPLOYEE_ID_KEY:TextField(cls.EMPLOYEE_ID_KEY).setUnique(), 
            cls.AWARD_ID_KEY:TextField(cls.AWARD_ID_KEY).setUnique(), 
            cls.EMPLOYEE_NAME_KEY:TextField(cls.EMPLOYEE_NAME_KEY),
            cls.DATE_KEY:DateField(cls.DATE_KEY),
            cls.QUANTITY_KEY:NumericField(cls.QUANTITY_KEY)
        })

        return VestingAggregator(contract_, filterDate)

    def __init__(self, contract: Contract, filterDate: str):
        self.result = {}
        self.contract = contract
        self.filterDate = filterDate

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
            self.QUANTITY_KEY:0                                 #TODO: support precision
         } 

    def isOnOrBeforeFilterDate(self, record: dict) -> bool:
        dateField = self.contract.getContractField(self.DATE_KEY)
        dateValue = dateField.getValue(record)
        return dateValue <= self.filterDate

    def incrementTotal(self, key: tuple, record: dict):
        quantityField = self.contract.getContractField(self.QUANTITY_KEY)
        self.result[key][self.QUANTITY_KEY] += quantityField.getValue(record)

    def getVestedTotals(self) -> list[str]:
        vestedTotals = []

        sortedKeys = sorted(self.result.keys(), key=lambda x: (x[0], x[1]))
        
        # Sort by employee ID, then by award ID
        for key in sortedKeys:
            resultRow = self.result[key]
            employeeId, awardId = key
            employeeName, quantity = resultRow[self.EMPLOYEE_NAME_KEY], resultRow[self.QUANTITY_KEY]
            
            vestedTotals.append(f'{employeeId},{employeeName},{awardId},{quantity}')
        
        return vestedTotals