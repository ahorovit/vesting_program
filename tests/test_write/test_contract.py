
import unittest

from vesting_program.write.contract import DateField, ValidationError


class TestDateField(unittest.TestCase):
    IDX = 'dateIdx'

    def setUp(self):
        self.field = DateField(self.IDX)

    def test_invalid_date(self):
        with self.assertRaises(ValidationError) as cm:
            self.field.getValue({self.IDX: 'invalid'})
            

if __name__ == '__main__':
    unittest.main()