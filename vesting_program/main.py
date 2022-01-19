import sys
from read.read import CsvReader
from write.write import VestingAggregator
from write.contract import Contract

def main():
    inputFile, filterDate, precision = parseArgs()

    headers = [
        VestingAggregator.EVENT_KEY,
        VestingAggregator.EMPLOYEE_ID_KEY,
        VestingAggregator.EMPLOYEE_NAME_KEY,
        VestingAggregator.AWARD_ID_KEY,
        VestingAggregator.DATE_KEY,
        VestingAggregator.QUANTITY_KEY 
    ]

    reader = CsvReader(inputFile, headers)
    aggregator = VestingAggregator.factory(filterDate, precision)

    for record in reader.getNextRecord():
        aggregator.pushRecord(record)

    for outputRow in aggregator.getVestedTotals():
        print(outputRow)

def parseArgs():
    # return "data/example1.csv", "2020-04-01" #TODO: Remove 

    numArgs = len(sys.argv)
    if numArgs == 3:
        _, inputFile, filterDate = sys.argv
        precision = 0
    elif numArgs == 4:
        _, inputFile, filterDate, precision = sys.argv
    else:
        raise InputError('Expecting inputFile, filterDate and optional precision parameters')

    # TODO: Validate args
    return inputFile, filterDate, int(precision)

class InputError(Exception):
    pass

if __name__ == '__main__':
    main()