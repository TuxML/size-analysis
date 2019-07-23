#!/usr/bin/env python3

# documentation to use kconfig: https://github.com/TuxML/ProjetIrma/tree/dev/miscellaneous/special-config/Kconfiglib
# make [ARCH=arch] scriptconfig SCRIPT=compareSizeResults.py SCRIPT_ARG=100
# make ARCH=x86 scriptconfig SCRIPT=compareSizeResults.py SCRIPT_ARG=100
# The second argument is the number of options to consider in the ML options list.


import csv
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


def produceOptionDocURL(option):
    global baseurloption
    global endurloption
    return baseurloption + option + endurloption


def writeResultsInFile(options, filename):
    with open(filename, 'w') as file:
        for opt in options:
            file.write("%s;%s\n"%(opt, produceOptionDocURL(opt)))


manualOptionsFile = open("optionsRelatedToSize.txt","r")
manualOptionsLines = manualOptionsFile.read().splitlines()
manualOptionsFile.close()

autoOptionsLists = pd.read_csv("feature_importanceRF.csv", nrows=nbRowsToAnalyse, usecols=[0]).values.tolist() # index_col=0, sep=',', dtype={0: str}, squeeze=True)
autoOptions = list(itertools.chain.from_iterable(autoOptionsLists))

optionsInBoth = list(filter(lambda opt: opt in autoOptions, manualOptionsLines))
optionsInManualOnly = list(filter(lambda opt: not (opt in autoOptions), manualOptionsLines))
optionsInAutoOnly = list(filter(lambda opt: not (opt in manualOptionsLines), autoOptions))

getDocumentation(kconf.top_node)

optionsInAutoOnlyWithoutDoc = list(filter(lambda opt: opt in helps and len(helps[opt]) == 0, optionsInAutoOnly))
optionsInAutoOnlyWithDoc = list(filter(lambda opt: opt in helps and len(helps[opt]) > 0, optionsInAutoOnly))

writeResultsInFile(optionsInBoth, 'optionsInBoth.csv')
writeResultsInFile(optionsInAutoOnlyWithoutDoc, 'optionsInAutoOnlyWithoutDoc.csv')
writeResultsInFile(optionsInAutoOnlyWithDoc, 'optionsInAutoOnlyWithDoc.csv')


