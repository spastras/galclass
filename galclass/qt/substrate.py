###########
# Imports #
###########

# System #

from __future__ import annotations

from typing import Optional

import os

from functools import partial

from PyQt6.QtCore import QSize, QObject, QRunnable, QThreadPool, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import QStyle, QCommonStyle, QFileDialog

# Local #

from .window import MainWindow
from ..fileio import readJSONFile, writeJSONFile
from ..misc import Console

###########
# Classes #
###########

#*******************#
# Input file loader #
#*******************#

class inputFileLoaderSignals(QObject):
    """
    Implements loaded and finished signals for inputFileLoader
    """

    # Class attributes
    finished=pyqtSignal(dict, dict, str)

class inputFileLoader(QRunnable):
    """
    Loads an input list file
    """

    def __init__(self, inputFile: str, outputFile: str):
        """
        Constructor
        """

        # Call super().__init__
        super(inputFileLoader, self).__init__()

        # Initialize the signals
        self.signals=inputFileLoaderSignals()

        # Evaluate arguments
        self.inputFile=inputFile
        self.outputFile=outputFile

        # Return
        return

    @pyqtSlot()
    def run(self):
        """
        Loads the input file
        """

        # Read JSON file
        fileDict=readJSONFile(self.inputFile)

        # Attempt to read previous output JSON file
        try:
            propertyDict=readJSONFile(self.outputFile)
        except:
            propertyDict={}

        # Emit finished signal
        self.signals.finished.emit(fileDict, propertyDict, self.outputFile)

        # Return
        return

#**************#
# Qt substrate #
#**************#

class QtSubstrate(QObject):
    """
    A class to be used as the substrate for the Qt application
    """

    def __init__(self, categoriesFile: str, outputFileSuffix: Optional[str] = "_classified.json", defaultWindowSize: QSize = QSize(1920, 1080)):
        """
        Constructor
        """

        # Evaluate arguments
        self.outputFileSuffix=outputFileSuffix
        self.defaultWindowSize=defaultWindowSize

        # Initialize attributes

        # Backend
        self.actionSubstrate=None
        self.loaderPool=QThreadPool()
        self.window=None

        # Status
        self.categoryWidgetsEnabled=False
        self.excludeClassified=True
        self.inputFileLoading=False
        
        # Data
        self.fileDict=None
        self.propertyDict=[]
        self.outputFile=None

        # Call super().__init__
        super().__init__()

        # Initialize the categories dictionary
        self.categoriesDict=readJSONFile(categoriesFile)

        # Return
        return
    
    def initMainWindow(self) -> None:
        """
        Initialize the main window
        """

        # Initialize action substrate
        self.__initActionSubstrate()

        # Initialize the main window
        self.window=MainWindow(self)
        self.window.resize(self.defaultWindowSize)
        self.window.show()

        # Return
        return
    
    def closeMainWindow(self) -> None:
        """
        Close the main window
        """

        # Close the window
        self.window.close()

        # Free the window handle
        self.window=None

        # Return
        return
    
    def __initActionSubstrate(self) -> None:
        """
        Initializes the Qt actions substrate
        """

        # Initialize action substrate
        self.actionSubstrate=QtActionSubstrate(self)

        # Enable the file actions
        self.actionSubstrate.setFileActionsEnabled(True)

        # Enable the navigation actions
        self.actionSubstrate.setNavigationActionsEnabled(False)

        # Return
        return
    
    def openFileDialog(self) -> None:
        """
        Opens the file load dialog
        """

        # Open the file dialog
        fileDialog=QFileDialog()
        inputFile=fileDialog.getOpenFileName(self.window, "Open JSON File", "", "JSON Files (*.json)")[0]

        # Open the specified file
        if(inputFile!=""):
            self.openInputFile(inputFile=inputFile)

        # Return
        return
    
    def openInputFile(self, inputFile: str) -> None:
        """
        Opens an input files

        Parameters
        ----------
        inputFile : str
            The path to the input file to open
        """

        # Check whether there are files being currently opened
        if(self.inputFileLoading):
            Console.printError("An input file is currently being loaded")
            return
        
        # Check whether the specifed file exists
        if(not (os.path.exists(inputFile))):
            Console.printError("The specified file doesn't exist")
            return
        
        # Set metadata
        self.inputFileLoading=True

        # Disable category widgets
        self.window.categoriesToolbar.toggleCategoryWidgets(False)

        # Disable actions
        self.actionSubstrate.setFileActionsEnabled(False)
        self.actionSubstrate.setNavigationActionsEnabled(False)

        # Determine the output filename
        outputFile=inputFile
        inputFileSuffixes=[".json", ".txt", ".lst", ".dat"]
        for inputFileSuffix in inputFileSuffixes:
            outputFile=outputFile.removesuffix(inputFileSuffix)
        outputFile=outputFile+self.outputFileSuffix

        # Initialize the input file loader
        loader=inputFileLoader(inputFile, outputFile)
        loader.signals.finished.connect(self.loadingDone)

        # Start the snapshot loader
        self.loaderPool.start(loader)

        # Return
        return
    
    def loadingDone(self, fileDict: dict, propertyDict: dict, outputFile: str) -> None:
        """
        Loading of a new file dictionary has been completed

        Parameters
        ----------
        fileDict : dict
            A dictionary with the information about the files of the galaxies to be classified
        propertyDict : dict
            A dictionary with previously determined properties of the galaxies to be classified
        outputFile : str
            The path to the file to use for the writing of the properties of the galaxies
        """

        # Evaluate arguments
        self.outputFile=outputFile

        # Set metadata
        self.inputFileLoading=False

        # Update the file dict
        self.fileDict=fileDict

        # Update the property dict
        if(propertyDict):
            self.propertyDict=propertyDict
        else:
            self.__initGalaxyProperties()

        # Notify the window
        self.window.dictUpdated()

        # Enable category widgets
        self.window.categoriesToolbar.toggleCategoryWidgets(True)

        # Enable actions
        self.actionSubstrate.setFileActionsEnabled(True)
        self.actionSubstrate.setNavigationActionsEnabled(True)

        # Return
        return
    
    def toggleExcludeClassified(self, enabled: bool) -> None:
        """
        Toggle the loading of only the unclassified galaxies
        """

        # Trigger the exclude classified
        self.excludeClassified=enabled

        # Load the next non classified galaxy
        if(self.excludeClassified):
            pass

        # Return
        return
    
    def switchGalaxy(self, increment: int) -> None:
        """
        Switch the currently loaded galaxy
        """

        # Switch galaxy
        self.window.loadGalaxy(self.window.igalaxy+increment)

        # Return
        return
    
    def switchFilter(self, increment: int) -> None:
        """
        Switch the currently loaded filter
        """

        # Switch filter
        self.window.loadFilter(self.window.ifilter+increment)

        # Return
        return
    
    def __initGalaxyProperties(self) -> None:

        # Initialize the property dictionary
        self.propertyDict={'galaxies':[]}

        # Propulate the property dictionary
        for igalaxy in range(len(self.fileDict['galaxies'])):
            self.propertyDict['galaxies'].append({'name':self.fileDict['galaxies'][igalaxy]['name'], 'categories':[], 'comments':""})
        
        # Write the property dictionary to file
        self.__writeOutputFile()

        # Return
        return
    
    def __writeOutputFile(self) -> None:

        # Write the property dictionary to file
        writeJSONFile(self.outputFile, self.propertyDict)

        # Return
        return
    
    def updateGalaxyProperties(self, igalaxy: int, categories: list, comments: str) -> None:
        """
        Updates the properties of the specified galaxy

        Parameters
        ----------
        igalaxy : int
            The ID of the galaxy the properties of which need to be updated
        categories : list
            A list with the categories of which the galaxy is a part
        comments : str
            Comments about the galaxy
        """

        # Update the properties of the specified galaxy
        self.propertyDict['galaxies'][igalaxy]['categories']=categories
        self.propertyDict['galaxies'][igalaxy]['comments']=comments

        # Write the property dictionary to file
        writeJSONFile(self.outputFile, self.propertyDict)

        # Return
        return

#*********************#
# Qt action substrate #
#*********************#

class QtActionSubstrate(QObject):
    """
    A class to be used as the substrate for the Qt actions
    """

    def __init__(self, substrate: QtSubstrate):
        """
        Constructor
        """

        # Evaluate arguments
        self.substrate=substrate

        # Call super().__init__
        super().__init__()

        # Initialize actions
        self.__initActions()

        # Return
        return
    
    def __initActions(self):
        """
        Initialize the Qt actions
        """

        # Initialize file actions
        self.__initFileActions()

        # Initialize navigation actions
        self.__initNavigationActions()

        # Return
        return
    
    def __initFileActions(self):
        """
        Initialize the Qt file actions
        """

        # Initialize file actions list
        self.fileActions=[]

        # Populate file actions list

        # Initialize the "Open File" action
        action=QAction("Open File", self)
        action.setCheckable(False)
        action.setShortcut(QKeySequence('Ctrl+O'))
        action.triggered.connect(self.substrate.openFileDialog)
        self.fileActions.append(action)

        # Return
        return
    
    def __initNavigationActions(self):
        """
        Initializes the navigation actions
        """

        # Initialize navigation actions list
        self.navigationActions=[]

        # Populate navigation actions list

        # Initialize the Qt common style
        style=QCommonStyle()

        # Initialize the galaxy navigation actions

        action=QAction("Exclude Classified", self)
        action.setCheckable(True)
        action.setChecked(True)
        action.toggled.connect(self.substrate.toggleExcludeClassified)
        self.navigationActions.append(action)

        action=QAction("Previous Galaxy", self)
        action.setData(-1)
        action.setCheckable(False)
        action.setShortcut(QKeySequence('Shift+Left'))
        action.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_ArrowLeft))
        action.triggered.connect(partial(self.substrate.switchGalaxy, action.data()))
        self.navigationActions.append(action)

        action=QAction("Next Galaxy", self)
        action.setData(1)
        action.setCheckable(False)
        action.setShortcut(QKeySequence('Shift+Right'))
        action.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_ArrowRight))
        action.triggered.connect(partial(self.substrate.switchGalaxy, action.data()))
        self.navigationActions.append(action)

        # Initialize the filter navigation actions

        action=QAction("Previous Filter", self)
        action.setData(-1)
        action.setCheckable(False)
        action.setShortcut(QKeySequence('Left'))
        action.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_ArrowLeft))
        action.triggered.connect(partial(self.substrate.switchFilter, action.data()))
        self.navigationActions.append(action)

        action=QAction("Next Filter", self)
        action.setData(1)
        action.setCheckable(False)
        action.setShortcut(QKeySequence('Right'))
        action.setIcon(style.standardIcon(QStyle.StandardPixmap.SP_ArrowRight))
        action.triggered.connect(partial(self.substrate.switchFilter, action.data()))
        self.navigationActions.append(action)

        # Return
        return
    
    def setFileActionsEnabled(self, enabled: bool):
        """
        Enable/Disable the file actions
        """

        # Enable/Disable file actions
        for action in self.fileActions:
            action.setEnabled(enabled)
            for object in action.associatedObjects():
                object.setEnabled(enabled)

        # Return
        return
    
    def setNavigationActionsEnabled(self, enabled: bool):
        """
        Enable/Disable the navigation actions
        """

        # Enable/Disable navigation actions
        for action in self.navigationActions:
            action.setEnabled(enabled)
            for object in action.associatedObjects():
                object.setEnabled(enabled)

        # Return
        return