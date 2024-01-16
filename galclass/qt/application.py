###########
# Imports #
###########

# System #

from typing import Optional

from PyQt6.QtWidgets import QApplication, QFileDialog

# Local #

from .substrate import QtSubstrate

#############
# Functions #
#############

#*******#
# Start #
#*******#

def start(categoriesFile: Optional[str] = None, inputFile: Optional[str] = None, outputFileSuffix: Optional[str] = "_classified.json") -> None:
    """
    Initializes the Qt application

    Parameters
    ----------
    categoriesFile : str, optional
        The path to the categories file (default is None)
    inputFile : str, optional
        The path to the input list file (default is None)
    outputFileSuffix : str, optional
        The suffix to be added to the input file path in order to form the filename of the output classification file (default is "_classified.json")
    """

    # Initialize the Qt substrate
    substrate=QtSubstrate(outputFileSuffix=outputFileSuffix)

    # Initialize the Qt application
    application=QApplication(["galclass"])

    # Get the categories file if needed
    if(categoriesFile==""):
        # Open the file dialog
        fileDialog=QFileDialog()
        categoriesFile=fileDialog.getOpenFileName(None, "Open categories JSON File", "", "JSON Files (*.json)")[0]
        # Parse the path to the categories file
        if(categoriesFile==""):
            categoriesFile=None
    
    # Use the specified categories file
    substrate.useCategoriesFile(categoriesFile=categoriesFile)

    # Initialize the main window
    substrate.initMainWindow()

    # Open input file
    if(inputFile is not None):
        substrate.openInputFile(inputFile)

    # Start the Qt event loop
    application.exec()

    # Return
    return