import unittest
from vesting_program.write.write import VestingAggregator
from vesting_program.write.contract import TextField, DateField, NumericField, Contract, ValidationError

 
class TestAggregator(unittest.TestCase):
    """Test class for Aggregator"""

    FILTER_DATE = '2021-01-01'

    RECORD_1 = {
        VestingAggregator.EVENT_KEY:VestingAggregator.VEST_VALUE,
        VestingAggregator.EMPLOYEE_ID_KEY:'E001',
        VestingAggregator.EMPLOYEE_NAME_KEY:'Alice Smith',
        VestingAggregator.AWARD_ID_KEY:'ISO-001',
        VestingAggregator.DATE_KEY:FILTER_DATE,
        VestingAggregator.QUANTITY_KEY:'1000'
    }
    RECORD_2 = {
        VestingAggregator.EVENT_KEY:VestingAggregator.VEST_VALUE,
        VestingAggregator.EMPLOYEE_ID_KEY:'E002',
        VestingAggregator.EMPLOYEE_NAME_KEY:'Bobby Jones',
        VestingAggregator.AWARD_ID_KEY:'NSO-001',
        VestingAggregator.DATE_KEY:FILTER_DATE,
        VestingAggregator.QUANTITY_KEY:'100'
    }
    RECORD_3 = {
        VestingAggregator.EVENT_KEY:VestingAggregator.VEST_VALUE,
        VestingAggregator.EMPLOYEE_ID_KEY:'E001',
        VestingAggregator.EMPLOYEE_NAME_KEY:'Alice Smith',
        VestingAggregator.AWARD_ID_KEY:'ISO-001',
        VestingAggregator.DATE_KEY:'2020-12-15',
        VestingAggregator.QUANTITY_KEY:'200'
    }
    RECORD_4 = {
        VestingAggregator.EVENT_KEY:VestingAggregator.VEST_VALUE,
        VestingAggregator.EMPLOYEE_ID_KEY:'E001',
        VestingAggregator.EMPLOYEE_NAME_KEY:'Alice Smith',
        VestingAggregator.AWARD_ID_KEY:'ISO-001',
        VestingAggregator.DATE_KEY:'2021-06-15',        # after filter date
        VestingAggregator.QUANTITY_KEY:'500'
    }
    RECORD_5 = {
        VestingAggregator.EVENT_KEY:VestingAggregator.VEST_VALUE,
        VestingAggregator.EMPLOYEE_ID_KEY:'E000',
        VestingAggregator.EMPLOYEE_NAME_KEY:'Baz FooBar',
        VestingAggregator.AWARD_ID_KEY:'ISO-001',
        VestingAggregator.DATE_KEY:'2021-06-15',        # after filter date
        VestingAggregator.QUANTITY_KEY:'1000000'
    }
    RECORD_6 = {
        VestingAggregator.EVENT_KEY:VestingAggregator.VEST_VALUE,
        VestingAggregator.EMPLOYEE_ID_KEY:'E001',
        VestingAggregator.EMPLOYEE_NAME_KEY:'Alice Smith',
        VestingAggregator.AWARD_ID_KEY:'ISO-002',       # new award for Alizce
        VestingAggregator.DATE_KEY:'2020-12-15',
        VestingAggregator.QUANTITY_KEY:'600'
    }
    RECORD_7 = {
        VestingAggregator.EVENT_KEY:VestingAggregator.CANCEL_VALUE, # subtract some award
        VestingAggregator.EMPLOYEE_ID_KEY:'E001',
        VestingAggregator.EMPLOYEE_NAME_KEY:'Alice Smith',
        VestingAggregator.AWARD_ID_KEY:'ISO-002',       
        VestingAggregator.DATE_KEY:'2020-12-15',
        VestingAggregator.QUANTITY_KEY:'200'
    }

    def setUp(self):
        self.aggregator = VestingAggregator.factory(self.FILTER_DATE)

    def test_aggregator_push(self):
        """Test aggregator functionality over the course of expected input records"""

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

        # Alice loses some of the second award -- reduce total
        self.aggregator.push(self.RECORD_7)
        expected[2] = 'E001,Alice Smith,ISO-002,400'
        self.assertEqual(expected, self.aggregator.getVestedTotals())

    def test_vested_total_never_negative(self):
        """CANCEL event should not push total below 0"""
        with self.assertRaises(ValidationError):
            self.aggregator.push(self.RECORD_7)

    def test_precision(self):
        cases = [
            [0, '1.02345', '1'],
            [1, '1.02345', '1.0'],
            [4, '1.02345', '1.0234'],
            [2, '1', '1.00']
        ]
        for case in cases:
            with self.subTest(case=case):
                precision, quantity, expected = case
                inputRecord = self.RECORD_1
                inputRecord[VestingAggregator.QUANTITY_KEY] = quantity
                aggregator = VestingAggregator.factory(self.FILTER_DATE, precision)
                aggregator.push(inputRecord)
                actual = aggregator.getVestedTotals()[0].split(',')[-1]
                self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()