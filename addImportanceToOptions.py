import csv

optionsFile = open("optionsRelatedToSize.txt","r")
lines = optionsFile.read().splitlines()

output = open("optionsAndImportance.csv","w+")

optImportance = []

with open('feature_importance.csv') as importanceFile:
    csv_reader = csv.reader(importanceFile, delimiter=',')

    optImportance = {rows[0]:rows[1] for rows in csv_reader}


for optionName in lines:
    if optionName in optImportance:
        output.write(f'{optionName},{optImportance[optionName]}\n')
    else:
        output.write(f'{optionName},None\n')

optionsFile.close()
