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
JUMP_LEFT_SEQ = '\u001b[100D'


results = []
start = time.time()

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
        userEmails = list(set(map(lambda v: v.User_email, sourceEntries)))
        successCount = 0
        currencies = set(map(lambda value: value.Currency, sourceEntries))
        currencyDepositSum = {}
        for currency in currencies:
            currencyDepositSum[currency] = 0.0
        # print("                                            ")
        for mail in userEmails:
            successfulEntries = list(
                filter(lambda e: e.User_email == mail and e.Success == 'Yes', sourceEntries))

            successfulEntriesCount = len(successfulEntries)

            if successfulEntriesCount > 0:
                successCount += 1

            for transaction in successfulEntries:
                tempValue = currencyDepositSum[transaction.Currency]
                tempValue += float(transaction.Amount)
                currencyDepositSum[transaction.Currency] = tempValue

            percent = str((float(userEmails.index(mail)) /
                          float(len(userEmails))) * 100)[0:5] + "%"
            formattedPercent = "Processing %s: %s" % (source, percent)
            print(JUMP_LEFT_SEQ, end='')
            print(formattedPercent, end='')
            sys.stdout.flush()

        totalCount = len(userEmails)
        successRate = str(
            (float(successCount) / float(totalCount)) * 100)[0:5] + "%"

        moneyResult = ''
        for item in currencyDepositSum:
            moneyResult += str(item) + ': ' + \
                str(currencyDepositSum[item]) + '\n'
        resultString = "\n\x1b[6;30;42m" + str(source) + "\x1b[0m" + "\nTotal unique users: " + \
            str(totalCount) + "\nSuccess transactions: " + \
            str(successCount) + "\n\x1b[0;33mSuccess Rate: " + \
            str(successRate) + "\x1b[0m\n" + moneyResult

        results.append(resultString)

print(JUMP_LEFT_SEQ, end='')
print("                                            ")
reportPath = os.path.split(TARGET_CSV_PATH)[
    0] + 'Report for ' + re.sub(r'\.\w+', '', os.path.split(TARGET_CSV_PATH)[1]) + '.txt'
reportFile = open(reportPath, 'w')
for result in results:
    print(result)

    strippedFromAttributes = re.sub(r'\[0;33m', '', result)
    strippedFromAttributes = re.sub(r'\[0m', '', strippedFromAttributes)
    strippedFromAttributes = re.sub(r'\[6;30;42m', '', strippedFromAttributes)

    reportFile.write(strippedFromAttributes + '\n')

reportFile.close()

print('👑')

end = time.time()
print("\nElapsed %s seconds" % (end - start))

