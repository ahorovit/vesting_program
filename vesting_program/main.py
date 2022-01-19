import sys
from read.read import CsvReader
from write.write import VestingAggregator
from write.contract import Contract

def main():
    inputFile, filterDate = parseArgs()

    headers = [
        VestingAggregator.EVENT_KEY,
        VestingAggregator.EMPLOYEE_ID_KEY,
        VestingAggregator.EMPLOYEE_NAME_KEY,
        VestingAggregator.AWARD_ID_KEY,
        VestingAggregator.DATE_KEY,
        VestingAggregator.QUANTITY_KEY 
    ]

    reader = CsvReader(inputFile, headers)
    aggregator = VestingAggregator.factory(filterDate)

    for record in reader.getNextRecord():
        aggregator.push(record)

    for outputRow in aggregator.getVestedTotals():
        print(outputRow)


def parseArgs():
    # return "data/example1.csv", "2020-04-01" #TODO: Remove 

    # Extract filepath, precision args
    if len(sys.argv) < 3:
        raise InputError('Expecting inputFile and filterDate parameters')

    # TODO: Validate args
    _, inputFile, filterDate = sys.argv 
    return (inputFile, filterDate)

class InputError(Exception):
    pass

if __name__ == '__main__':
    main()