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

        rowCount = 0
        for csvRow in self.reader.getNextRecord():
            rowCount += 1
            self.assertIsInstance(csvRow, list, 'expected list type')
            self.assertEqual(len(csvRow), 6, 'expected 6 elements')
        self.assertEqual(rowCount, 2, 'expected 2 rows')





if __name__ == '__main__':
    unittest.main()