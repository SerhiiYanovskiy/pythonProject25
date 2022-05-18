import sys
import csv
from collections import namedtuple


class DataEntry:
    def __init__(self, dataArray, paramNames):
        for prop, data in zip(paramNames, dataArray):
            self.__dict__[prop] = data

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


TARGET_CSV_PATH = "payments_2022_05_18-13_28 (3).csv"

with open(TARGET_CSV_PATH) as csvfile:
    reader = csv.DictReader(csvfile)
    dataEntries = []
    for row in reader:
        rawValues = []
        for fieldname in reader.fieldnames:
            rawValues.append(row[fieldname])
        dataEntries.append(DataEntry(rawValues, map(
            lambda name: name.replace(' ', "_"), reader.fieldnames)))

    sources = {}

    for item in dataEntries:
        sources[item.Source] = {}

    for source in sources:
        sourceEntries = list(filter(
            lambda value: value.Source == source, dataEntries))
        print('\n-------------   ' + "\x1b[6;30;42m" + source + "\x1b[0m")

        uniqueDays = {}

        for entry in sourceEntries:
            createdAtDate = entry.Created_at
            dayOfCreatedAtDate = createdAtDate[0:10]
            uniqueDays[dayOfCreatedAtDate] = list()

        for day in uniqueDays:
            entriesThisDay = []
            for entry in sourceEntries:
                if day in entry.Created_at:
                    entriesThisDay.append(entry)

            print('Date: ' + day)
            print('Overall transactions: ' + str(len(entriesThisDay)))
            successfulTransactions = list(filter(lambda value: value.Success == 'Yes', entriesThisDay))
            print('Successful transactions: ' + str(len(successfulTransactions)))
            percent = (len(successfulTransactions) / len(entriesThisDay)) * 100
            print('Successful transactions rate: \x1b[0;33m' + str(percent) + '%\x1b[0m\n')
