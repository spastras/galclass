###########
# Imports #
###########

# System #

from typing import Optional

from PyQt6.QtWidgets import QApplication

# Local #

from .substrate import QtSubstrate

#############
# Functions #
#############

#*******#
# Start #
#*******#

def start(categoriesFile: str, inputFile: Optional[str] = None, outputFileSuffix: Optional[str] = "_classified.json") -> None:
    """
    Initializes the Qt application

    Parameters
    ----------
    categoriesFile : str
        The path to the categories file
    inputFile : str, optional
        The path to the input list file (default is None)
    outputFileSuffix : str, optional
        The suffix to be added to the input file path in order to form the filename of the output classification file (default is "_classified.json")
    """

    # Initialize the Qt substrate
    substrate=QtSubstrate(categoriesFile=categoriesFile, outputFileSuffix=outputFileSuffix)

    # Initialize the Qt application
    application=QApplication(["galclass"])

    # Initialize the main window
    substrate.initMainWindow()

    # Open input file
    if(inputFile is not None):
        substrate.openInputFile(inputFile)

    # Start the Qt event loop
    application.exec()

    # Return
    return