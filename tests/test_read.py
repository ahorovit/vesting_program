import unittest
import os
from vesting_program.read.read import CsvReader, HeaderMismatchError

class TestCsvReader(unittest.TestCase):
    def setUp(self):
        currentDir = os.path.dirname(__file__)
        exampleCsv = os.path.join(currentDir, 'example.csv')
        self.header = ['event', 'id', 'name']
        self.reader = CsvReader(exampleCsv, self.header)

    def test_simple_read(self):
        """Tests CsvReader's Generator capability"""
        rowCount = 0
        for csvRow in self.reader.getNextRecord():
            rowCount += 1
            expectedRow = {'event':'VEST', 'id':'E001', 'name':'Alice'}
            self.assertEqual(csvRow, expectedRow, 'csvRow does not match')
        self.assertEqual(rowCount, 2, 'expected 2 rows')

    def test_column_count_check(self):
        """Tests CsvReader's enforcement of header count matching row length"""
        self.reader.header.append('foo')

        with self.assertRaises(HeaderMismatchError):
            for csvRow in self.reader.getNextRecord():
                pass


if __name__ == '__main__':
    unittest.main()