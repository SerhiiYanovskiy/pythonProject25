import sys
import csv
import time
import os
import re
from collections import namedtuple


class DataEntry:
    def __init__(self, dataArray, paramNames):
        for prop, data in zip(paramNames, dataArray):
            self.__dict__[prop] = data


TARGET_CSV_PATH = "payments_2022_05_18-13_28 (3).csv"

with open(TARGET_CSV_PATH) as csvfile:
    reader = csv.DictReader(csvfile)
    dataEntries = []
    for row in reader:
        rawValues = []
        for fieldname in reader.fieldnames:
            rawValues.append(row[fieldname])
        dataEntries.append(
            DataEntry(rawValues,
                      map(
                          lambda name: name.replace(' ', "_"),
                          reader.fieldnames
                      )
                      )
        )

    sources = {}

    for item in dataEntries:
        sources[item.Source] = {}

    for source in sources:
        sourceEntries = list(
            filter(
                lambda value: value.Source == source,
                dataEntries
            )
        )

        successfulTransactions = list(
            filter(
                lambda value: value.Success == 'Yes', sourceEntries
            )
        )
        succesesCount = len(successfulTransactions)

        failsOrPendingCount = len(list(filter(
            lambda value: value.Success != 'Yes', sourceEntries)))

        successRate = str(
            (float(succesesCount) / float(len(sourceEntries))) * 100)[0:5] + '%'

        sourceResult = '\x1b[6;30;42m' + source + ':' + '\x1b[0m' + '\nTotal transactions: ' + \
            str(len(sourceEntries)) + '\nTotal Success: ' + \
            str(succesesCount) + \
            '\n\x1b[0;33mSuccess Rate: ' + successRate + '\x1b[0m'

        currencies = set(map(lambda value: value.Currency, sourceEntries))

        currencyDepositSum = {}

        for currency in currencies:
            currencyDepositSum[currency] = 0.0

        for transaction in successfulTransactions:
            tempValue = currencyDepositSum[transaction.Currency]
            tempValue += float(transaction.Amount)
            currencyDepositSum[transaction.Currency] = tempValue

        moneyResult = '\n'

        for item in currencyDepositSum:
            moneyResult += str(item) + ': ' + \
                str(currencyDepositSum[item]) + '\n'

        sourceResult += moneyResult


    generalTransactionsCount = len(dataEntries)


    generalSuccessfulCount = len(list(
        filter(
            lambda v: v.Success == 'Yes',
            dataEntries
        )
    ))
    generalSuccessfulRate = str(
        float(generalSuccessfulCount) / float(generalTransactionsCount) * 100)[0:5] + '%'




