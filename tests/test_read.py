import unittest
import os

from vesting_program.read.read import CsvReader

class TestCsvReader(unittest.TestCase):

    def setUp(self):
        currentDir = os.path.dirname(__file__)
        exampleCsv = os.path.join(currentDir, 'example.csv')
        self.reader = CsvReader(exampleCsv)


    def test_simple_read(self):
        """Tests CsvReader's Generator capability"""
        for row in self.reader.getNextRecord():
            print(row)





if __name__ == '__main__':
    unittest.main()