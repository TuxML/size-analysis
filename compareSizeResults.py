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
                helps[node.item.name] = str(node.help)

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
def writeResultsInFile(options, filename):
    with open(filename, 'w') as file:
        for opt in options:
            file.write("%s,%s\n"%(opt, produceOptionDocURL(opt)))

# Reading the options manually spotted
manualOptionsFile = open("optionsRelatedToSize.txt","r")
manualOptionsLines = manualOptionsFile.read().splitlines()
manualOptionsFile.close()

# Reading the options automatically spotted
autoOptionsLists = pd.read_csv("feature_importanceRF.csv", nrows=nbRowsToAnalyse, usecols=[0]).values.tolist() # index_col=0, sep=',', dtype={0: str}, squeeze=True)
# flatting the list of lists
autoOptions = list(itertools.chain.from_iterable(autoOptionsLists))

# Computing the options spotted by both
optionsInBoth = list(filter(lambda opt: opt in autoOptions, manualOptionsLines))
# Computing the options not present in the feature_importance list
optionsInManualOnly = list(filter(lambda opt: not (opt in autoOptions), manualOptionsLines))
# Computing the options not present in the optionsRelatedToSize list
optionsInAutoOnly = list(filter(lambda opt: not (opt in manualOptionsLines), autoOptions))

# Extracting the documentation from the kernel
getDocumentation(kconf.top_node)

# Computing the options of feature_importance, not present in optionsRelatedToSize, that do not have documentation
optionsInAutoOnlyWithoutDoc = list(filter(lambda opt: opt in helps and len(helps[opt]) == 0, optionsInAutoOnly))
# Computing the options of feature_importance, not present in optionsRelatedToSize, that have documentation
optionsInAutoOnlyWithDoc = list(filter(lambda opt: opt in helps and len(helps[opt]) > 0, optionsInAutoOnly))

# Writing the results
writeResultsInFile(optionsInBoth, 'optionsInBoth.csv')
writeResultsInFile(optionsInAutoOnlyWithoutDoc, 'optionsInAutoOnlyWithoutDoc.csv')
writeResultsInFile(optionsInAutoOnlyWithDoc, 'optionsInAutoOnlyWithDoc.csv')
