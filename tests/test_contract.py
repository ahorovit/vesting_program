
import unittest
from vesting_program.write.contract import Contract, DateField, EnumField, TextField, NumericField, ValidationError

class TestDateField(unittest.TestCase):
    IDX = 'dateIdx'

    def setUp(self):
        self.field = DateField(self.IDX)

    def test_invalid_date(self):
        with self.assertRaises(ValidationError):
            self.field.getValue({self.IDX: 'invalid'})


class TestTextField(unittest.TestCase):
    IDX = 'textIdx'

    def setUp(self):
        self.field = TextField(self.IDX)
    
    def test_invalid_text(self):
        with self.assertRaises(ValidationError):
            self.field.getValue({self.IDX: 123})


class TestNumericField(unittest.TestCase):
    IDX = 'numIdx'

    def setUp(self):
        self.field = NumericField(self.IDX)

    def test_invalid_numeric(self):
        with self.assertRaises(ValidationError):
            self.field.getValue({self.IDX: 'baz'})

    def test_precision(self):
        cases = [
            [0, '1.02345', 1],
            [1, '1.02345', 1.0],
            [4, '1.02345', 1.0234],
            [2, '1', 1.0],
            [1, '700.75', 700.7]
        ]

        for case in cases:
            with self.subTest(case=case):
                precision, input, expected = case
                field = NumericField(self.IDX, precision)
                actual = field.getValue({self.IDX: input})
                self.assertEqual(actual, expected)


class TestEnumField(unittest.TestCase):
    IDX = 'enumIdx'

    def setUp(self):
        self.field = EnumField(self.IDX, ['foo', 'bar'])

    def test_invalid_enum(self):
        with self.assertRaises(ValidationError):
            self.field.getValue({self.IDX:'baz'})


class TestContract(unittest.TestCase):
    UNIQUE_DATE = '2021-01-01'
    RECORD = {'fooDate':UNIQUE_DATE, 'bar':'baz'}

    def setUp(self):
        fields = {
            'fooDate':DateField('fooDate').setUnique(), 
            'bar':TextField('bar')
        }
        self.contract = Contract(fields)

    def test_unique_key(self):
        self.assertEqual((self.UNIQUE_DATE,), self.contract.getUniqueKey(self.RECORD))

    def test_get_field(self):
        self.assertIsInstance(self.contract.getContractField('fooDate'), DateField)


if __name__ == '__main__':
    unittest.main()