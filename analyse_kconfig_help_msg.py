#!/usr/bin/python3

# documentation to use kconfig: https://github.com/TuxML/ProjetIrma/tree/dev/miscellaneous/special-config/Kconfiglib
# make [ARCH=arch] scriptconfig SCRIPT=analyse_kconfig_help_msg.py
# make ARCH=x86 scriptconfig SCRIPT=analyse_kconfig_help_msg.py

import sys
from kconfiglib import Kconfig, Symbol
import csv
import numpy as np 
import matplotlib as mpl 
import matplotlib.pyplot as plt 

## agg backend is used to create plot as a .png file
mpl.use('agg')


#the kconfig file produced by make and provided as argument
kconf = Kconfig(sys.argv[1])
# the help dict: keys are config names, values are help messages (when exist)
helps = {}
# counting options not documented
undoc = 0
# The number of options
optionsCount = 0
docStats = []

# the internal method that analyses the documentation to
# identify these options that explicitly refer to a change in
# the kernel size
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


# The internal method that analyses the documentation
# to compute stats on it based on the number of words for each options
def help_msg_stat(node):
    global docStats

    while node:
        if isinstance(node.item, Symbol):
            if str(node.help) == "None":
                docStats.append(0)
            else:
                docStats.append(len(node.help.split()))

        if node.list:
            help_msg_stat(node.list)

        node = node.next


# Launcher for computing stats on the documentation
def launch_stat_help():
    global kconf
    global docStats
    help_msg_stat(kconf.top_node)

    fig = plt.figure(figsize=(5, 5), dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    bp = ax.boxplot(docStats)
    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.xlabel('Options documentation', fontsize=12)
    plt.ylabel('# of words', fontsize=12)
    fig.savefig('plotHelpWords.png')


# launcher for identifying options related to the kernel size
def launch_analyse_help_size():
    global kconf
    global helps
    global optionsCount

    analyse_help(kconf.top_node)

    # Saving the dic as an CSV file
    with open('helpMsgs.csv', 'w') as file:
        for key in helps.keys():
            file.write("%s;%s\n"%(key,helps[key]))

    print("Options: %d"%optionsCount)
    print("Options not documented: %d"%undoc)



#launch_analyse_help_size()
launch_stat_help()
