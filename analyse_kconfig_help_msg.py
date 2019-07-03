#!/usr/bin/python3

# documentation to use kconfig: https://github.com/TuxML/ProjetIrma/tree/dev/miscellaneous/special-config/Kconfiglib
# make [ARCH=arch] scriptconfig SCRIPT=analyse_kconfig_help_msg.py

import sys
from kconfiglib import Kconfig, Symbol
import csv

#the kconfig file produced by make and provided as argument
kconf = Kconfig(sys.argv[1])
# the help dict: keys are config names, values are help messages (when exist)
helps = {}
# counting options not documented
undoc = 0
# The number of options
optionsCount = 0

def analyse_help(node):
    global undoc
    global helps
    global optionsCount

    while node:
        if isinstance(node.item, Symbol):
            optionsCount = optionsCount + 1
            if str(node.help) == "None":
                undoc = undoc + 1
            else:
                helpMsg = str(node.help)
                helps[node.item.name] = helpMsg.replace("\n"," ").replace(";", ".").replace('"', "")

        if node.list:
            analyse_help(node.list)

        node = node.next

analyse_help(kconf.top_node)

# Saving the dic as an CSV file
with open('helpMsgs.csv', 'w') as file:
    for key in helps.keys():
        file.write("%s;%s\n"%(key,helps[key]))

print("Options: %d"%optionsCount)
print("Options not documented: %d"%undoc)
