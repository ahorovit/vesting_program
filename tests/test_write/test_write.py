import unittest
from vesting_program.write.write import VestingAggregator
import vesting_program.write.contract as contract

class TestAggregator(unittest.TestCase):
    """Test class for Aggregator"""

    FILTER_DATE = '2021-01-01'

    RECORD_1 = {
        'VEST':'VEST',
        VestingAggregator.EMPLOYEE_ID_KEY:'E001',
        VestingAggregator.EMPLOYEE_NAME_KEY:'Alice Smith',
        VestingAggregator.AWARD_ID_KEY:'ISO-001',
        VestingAggregator.DATE_KEY:FILTER_DATE,
        VestingAggregator.QUANTITY_KEY:'1000'
    }
    RECORD_2 = {
        'VEST':'VEST',
        VestingAggregator.EMPLOYEE_ID_KEY:'E002',
        VestingAggregator.EMPLOYEE_NAME_KEY:'Bobby Jones',
        VestingAggregator.AWARD_ID_KEY:'NSO-001',
        VestingAggregator.DATE_KEY:FILTER_DATE,
        VestingAggregator.QUANTITY_KEY:'100'
    }
    RECORD_3 = {
        'VEST':'VEST',
        VestingAggregator.EMPLOYEE_ID_KEY:'E001',
        VestingAggregator.EMPLOYEE_NAME_KEY:'Alice Smith',
        VestingAggregator.AWARD_ID_KEY:'ISO-001',
        VestingAggregator.DATE_KEY:'2020-12-15',
        VestingAggregator.QUANTITY_KEY:'200'
    }
    RECORD_4 = {
        'VEST':'VEST',
        VestingAggregator.EMPLOYEE_ID_KEY:'E001',
        VestingAggregator.EMPLOYEE_NAME_KEY:'Alice Smith',
        VestingAggregator.AWARD_ID_KEY:'ISO-001',
        VestingAggregator.DATE_KEY:'2021-06-15',        # after filter date
        VestingAggregator.QUANTITY_KEY:'500'
    }
    RECORD_5 = {
        'VEST':'VEST',
        VestingAggregator.EMPLOYEE_ID_KEY:'E000',
        VestingAggregator.EMPLOYEE_NAME_KEY:'Baz FooBar',
        VestingAggregator.AWARD_ID_KEY:'ISO-001',
        VestingAggregator.DATE_KEY:'2021-06-15',        # after filter date
        VestingAggregator.QUANTITY_KEY:'1000000'
    }
    RECORD_6 = {
        'VEST':'VEST',
        VestingAggregator.EMPLOYEE_ID_KEY:'E001',
        VestingAggregator.EMPLOYEE_NAME_KEY:'Alice Smith',
        VestingAggregator.AWARD_ID_KEY:'ISO-002',       # new award for Alizce
        VestingAggregator.DATE_KEY:'2020-12-15',
        VestingAggregator.QUANTITY_KEY:'600'
    }

    CONTRACT_FIELDS = {
        VestingAggregator.EMPLOYEE_ID_KEY:contract.TextField(VestingAggregator.EMPLOYEE_ID_KEY).setUnique(), 
        VestingAggregator.AWARD_ID_KEY:contract.TextField(VestingAggregator.AWARD_ID_KEY).setUnique(), 
        VestingAggregator.EMPLOYEE_NAME_KEY:contract.TextField(VestingAggregator.EMPLOYEE_NAME_KEY),
        VestingAggregator.DATE_KEY:contract.DateField(VestingAggregator.DATE_KEY),
        VestingAggregator.QUANTITY_KEY:contract.NumericField(VestingAggregator.QUANTITY_KEY)
    }

    def setUp(self):
        self.contract = contract.Contract(self.CONTRACT_FIELDS)
        self.aggregator = VestingAggregator(self.contract, self.FILTER_DATE)

    def test_aggregator_push(self):
        expected = []

        # push first record
        self.aggregator.push(self.RECORD_1)
        expected.append('E001,Alice Smith,ISO-001,1000')
        self.assertEqual(expected, self.aggregator.getVestedTotals())

        # push second record -- distinct from first
        self.aggregator.push(self.RECORD_2)
        expected.append('E002,Bobby Jones,NSO-001,100')
        self.assertEqual(expected, self.aggregator.getVestedTotals())

        # push third record -- First row is updated
        self.aggregator.push(self.RECORD_3)
        expected[0] = 'E001,Alice Smith,ISO-001,1200' #increased by 200
        self.assertEqual(expected, self.aggregator.getVestedTotals())

        # fourth record is after filter date -- should not update result
        self.aggregator.push(self.RECORD_4)
        self.assertEqual(expected, self.aggregator.getVestedTotals())

        # fifth record introduces new employee, but is after filter date
        self.aggregator.push(self.RECORD_5)
        expected.insert(0, 'E000,Baz FooBar,ISO-001,0')
        self.assertEqual(expected, self.aggregator.getVestedTotals())

        # Alice gets second award -- new row
        self.aggregator.push(self.RECORD_6)
        expected.insert(2, 'E001,Alice Smith,ISO-002,600')
        self.assertEqual(expected, self.aggregator.getVestedTotals())

if __name__ == '__main__':
    unittest.main()