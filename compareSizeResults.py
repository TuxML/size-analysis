#!/usr/bin/env python3

# documentation to use kconfig: https://github.com/TuxML/ProjetIrma/tree/dev/miscellaneous/special-config/Kconfiglib
# make [ARCH=arch] scriptconfig SCRIPT=compareSizeResults.py SCRIPT_ARG=100
# make ARCH=x86 scriptconfig SCRIPT=compareSizeResults.py SCRIPT_ARG=100
# The second argument is the number of options to consider in the ML options list.


import pandas as pd
import itertools
from kconfiglib import Kconfig, Symbol
import sys

if len(sys.argv) < 3:
    sys.exit("Usage: make ARCH=x86 scriptconfig SCRIPT=compareSizeResults.py SCRIPT_ARG=100")

# the help dict: keys are config names, values are help messages (when exist)
helps = {}
kconf = Kconfig(sys.argv[1])
nbRowsToAnalyse = int(sys.argv[2])
baseurloption = "https://cateee.net/lkddb/web-lkddb/"
endurloption = ".html"


# Extracts the documentation from Kconfig
def getDocumentation(node):
    global kconf

    while node:
        if isinstance(node.item, Symbol):
            if str(node.help) == "None":
                helps[node.item.name] = ""
            else:
                helps[node.item.name] = str(node.help).replace("\n"," ").replace(";", ".").replace('"', "")

        if node.list:
            getDocumentation(node.list)

        node = node.next

# Produces an URL to look at an option documentation
def produceOptionDocURL(option):
    global baseurloption
    global endurloption
    return baseurloption + option + endurloption

# write the results of the analysis in a file
# options: the list of options to write
# filename: the filename to use
# withDoc: whether the kernel doc must be included
# computeRankingOption: a lambda to execute. Format: opt => None or a string
def writeResultsInFile(options, filename, withDoc, computeRankingOption):
    global helps
    with open(filename, 'w') as file:
        for opt in options:
            doc = helps[opt] if withDoc and opt in helps else ""
            value = computeRankingOption(opt) if computeRankingOption != None and computeRankingOption(opt) != None else ""

            file.write("%s,%s,%s,%s\n"%(opt, produceOptionDocURL(opt), value, '"' + doc + '"'))

# Reading the options manually spotted
manualOptionsFile = open("optionsRelatedToSize.txt","r")
manualOptionsLines = manualOptionsFile.read().splitlines()
manualOptionsFile.close()

# Reading the `nbRowsToAnalyse` first options automatically spotted (options name only)
autoOptionsLists = pd.read_csv("feature_importanceRF.csv", nrows=nbRowsToAnalyse, usecols=[0]).values.tolist()
# flatting the list of lists
autoOptions = list(itertools.chain.from_iterable(autoOptionsLists))

# Reading ALL the options automatically spotted (options name + importance value)
# autoOptionsDict = pd.read_csv("feature_importanceRF.csv", sep=',', header=None, index_col=0, names=["option", "importance"])['importance'].to_dict()
autoOptionsDataFrame = pd.read_csv("feature_importanceRF.csv", sep=',', header=None, names=["option", "importance", "ranking"], index_col=0)
# creating a new column with the ranking of the option
idx = [i for i in range(1, len(autoOptionsDataFrame) + 1)]
# Adding the new column in the data frame
autoOptionsDataFrame['ranking'] = idx
# transforming the data frame into a dict
autoOptionsDict = autoOptionsDataFrame.to_dict('index')

# Computing the options spotted by both
optionsInBoth = list(filter(lambda opt: opt in autoOptions, manualOptionsLines))
# Computing the options not present in the feature_importance list
optionsInManualOnly = list(filter(lambda opt: not (opt in autoOptions), manualOptionsLines))
# Computing the options not present in the optionsRelatedToSize list
optionsInAutoOnly = list(filter(lambda opt: not (opt in manualOptionsLines), autoOptions))
# Computing the options not present in the feature_importance list but present in the kernel
optionsKernelNotInAuto = list(filter(lambda opt: not (opt in autoOptions), helps.keys()))

# Extracting the documentation from the kernel
getDocumentation(kconf.top_node)

# Computing the options of `feature_importance`, not present in `optionsRelatedToSize`, that do not have documentation
optionsInAutoOnlyWithoutDoc = list(filter(lambda opt: opt in helps and len(helps[opt]) == 0, optionsInAutoOnly))
# Computing the options of `feature_importance`, not present in `optionsRelatedToSize`, that have documentation
optionsInAutoOnlyWithDoc = list(filter(lambda opt: opt in helps and len(helps[opt]) > 0, optionsInAutoOnly))

# Writing the results
writeResultsInFile(optionsInBoth, 'optionsInBoth.csv', False, lambda opt: str(autoOptionsDict[opt]['ranking']) if opt in autoOptionsDict else None)
writeResultsInFile(optionsInAutoOnlyWithoutDoc, 'optionsInAutoOnlyWithoutDoc.csv', False, lambda opt: None)
writeResultsInFile(optionsInAutoOnlyWithDoc, 'optionsInAutoOnlyWithDoc.csv', True, lambda opt: None)
writeResultsInFile(optionsKernelNotInAuto, 'optionsKernelNotInAuto.csv', True, lambda opt: None)
