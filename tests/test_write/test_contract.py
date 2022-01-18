
import unittest
import vesting_program.write.contract as contract


class TestDateField(unittest.TestCase):
    IDX = 'dateIdx'

    def setUp(self):
        self.field = contract.DateField(self.IDX)

    def test_invalid_date(self):
        with self.assertRaises(contract.ValidationError):
            self.field.getValue({self.IDX: 'invalid'})


class TestTextField(unittest.TestCase):
    IDX = 'textIdx'

    def setUp(self):
        self.field = contract.TextField(self.IDX)
    
    def test_invalid_text(self):
        with self.assertRaises(contract.ValidationError):
            self.field.getValue({self.IDX: 123})

class TestNumericField(unittest.TestCase):
    IDX = 'numIdx'

    def setUp(self):
        self.field = contract.NumericField(self.IDX)

    def test_invalid_numeric(self):
        with self.assertRaises(contract.ValidationError):
            self.field.getValue({self.IDX: 'baz'})


class TestContract(unittest.TestCase):
    UNIQUE_DATE = '2021-01-01'
    RECORD = {'fooDate':UNIQUE_DATE, 'bar':'baz'}

    def setUp(self):
        fields = {
            'fooDate':contract.DateField('fooDate').setUnique(), 
            'bar':contract.TextField('bar')
        }
        self.contract = contract.Contract(fields)

    def test_unique_key(self):
        self.assertEqual((self.UNIQUE_DATE,), self.contract.getUniqueKey(self.RECORD))


if __name__ == '__main__':
    unittest.main()