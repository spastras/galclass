#!/usr/bin/env python3

###########
# Imports #
###########

# System #

import sys

# Local #

from . import __version__

from . import qt
from .misc import Console

#############
# Functions #
#############

#*******#
# Usage #
#*******#

def usage():
    """
    Prints the command line usage information for galclass
    """
    Console.newLine()
    Console.printInfo("Usage: galclass [-c <categories_file>] [-i <input_file>] [-o <output_file_suffix>] [--graphical-only]")
    Console.newLine()
    Console.printInfo("[-c <categories_file>]\t->\t[optional] categories file (None)")
    Console.printInfo("[-i <input_file>]\t\t->\t[optional] input list file (None)")
    Console.printInfo("[-o <output_file_suffix>]\t->\t[optional] output classification file suffix ('_classificied.json')")
    Console.printInfo("[--graphical-only]\t\t->\t[optional] use the Graphical User Interface to get the path to the categories file")
    return

#******#
# Main #
#******#

def main(argv=sys.argv[1:]):
    """
    Main function
    """

    # Print startup banner

    versionStr=str(__version__)

    Console.printInfo("-============"+('='*len(versionStr))+"==-")
    Console.printInfo("-= galclass v"+versionStr+" =-")
    Console.printInfo("-============"+('='*len(versionStr))+"==-")
    Console.newLine()

    # Set default values of command line arguments

    categoriesFile=None
    inputFile=None
    outputFileSuffix="_classified.json"
    graphicalOnly=False

    # Evaluate Command Line Arguments

    Console.pushJob("Evaluating command line arguments...")

    # Determine the number of the specified command line arguments
    argc=len(argv)

    # Handle the help argument
    if(argc==1):
        if((argv[0]=="-h")or(argv[0]=="--help")):
            Console.popJob(success=True)
            usage()
            sys.exit(0)
    
    # Evaluate command line arguments
    iarg=0
    while(iarg<argc):
        if((argv[iarg]=="-c")and(iarg+1<argc)):
            categoriesFile=argv[iarg+1]
            iarg=iarg+1
        elif((argv[iarg]=="-i")and(iarg+1<argc)):
            inputFile=argv[iarg+1]
            iarg=iarg+1
        elif((argv[iarg]=="-o")and(iarg+1<argc)):
            outputFileSuffix=argv[iarg+1]
            iarg=iarg+1
        elif((argv[iarg]=="--graphical-only")):
            graphicalOnly=True
        else:
            Console.popJob(success=False)
            Console.printError(f"Unknown argument: \"{argv[iarg]}\"")
            sys.exit(1)
        iarg=iarg+1
    
    # Check whether the categories file is to be specified in a graphical way
    if(graphicalOnly):
        categoriesFile=""
    
    Console.popJob(success=True)

    # Inititalize the Qt interface

    qt.start(categoriesFile=categoriesFile, inputFile=inputFile, outputFileSuffix=outputFileSuffix)
    
    # That's all folks!

    Console.printWarning("Bye!")
    sys.exit(0)

#********************#
# Call main function #
#********************#

if __name__ == "__main__":
    main()