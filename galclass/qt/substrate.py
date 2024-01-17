###########
# Imports #
###########

# System #

from __future__ import annotations

from typing import Optional

import os

from functools import partial

import numpy as np

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
    finished=pyqtSignal(dict, dict, str, str)

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
        
        # Determine the path to the input root directory
        inputRootDir=os.path.abspath(os.path.dirname(os.path.expanduser(self.inputFile)))

        # Emit finished signal
        self.signals.finished.emit(fileDict, propertyDict, inputRootDir, self.outputFile)

        # Return
        return

#**************#
# Qt substrate #
#**************#

class QtSubstrate(QObject):
    """
    A class to be used as the substrate for the Qt application
    """

    def __init__(self, outputFileSuffix: Optional[str] = "_classified.json", defaultWindowSize: QSize = QSize(1920, 1080)):
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
        self.inputFileLoading=False
        
        # Data
        self.fileDict=None
        self.classified=None
        self.propertyDict=[]
        self.inputRootDir=None
        self.outputFile=None

        # Call super().__init__
        super().__init__()

        # Return
        return
    
    def useCategoriesFile(self, categoriesFile: Optional[str] = None) -> None:
        """
        Use the specified categories file

        Parameters
        ----------
        categoriesFile : str, optional
            The path to the categories file to use (default is None)
        """

        # Initialize the categories dictionary
        if(categoriesFile is not None):
            self.categoriesDict=readJSONFile(categoriesFile)
            self.excludeClassified=True
        else:
            self.categoriesDict={"categories": []}
            self.excludeClassified=False

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

        # Disable the navigation actions
        self.actionSubstrate.setExclusionNavigationActionEnabled(False)
        self.actionSubstrate.setLoadNavigationActionsEnabled(False)

        # Return
        return
    
    def openFileDialog(self) -> None:
        """
        Opens the file load dialog
        """

        # Open the file dialog
        fileDialog=QFileDialog()
        inputFile=fileDialog.getOpenFileName(self.window, "Open input file list JSON File", "", "JSON Files (*.json)")[0]

        # Open the specified file
        if(inputFile!=""):
            self.openInputFile(inputFile=inputFile)

        # Return
        return
    
    def openInputFile(self, inputFile: str) -> None:
        """
        Opens an input file

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

        # Unload the current galaxy
        self.window.loadGalaxy(None)

        # Disable actions
        self.actionSubstrate.setFileActionsEnabled(False)
        self.actionSubstrate.setExclusionNavigationActionEnabled(False)

        # Determine the output filename
        outputFile=inputFile
        inputFileSuffixes=[".json", ".txt", ".lst", ".dat"]
        for inputFileSuffix in inputFileSuffixes:
            # outputFile=outputFile.removesuffix(inputFileSuffix)
            if(outputFile.endswith(inputFileSuffix)):
                outputFile=outputFile[:-len(inputFileSuffix)]
        outputFile=outputFile+self.outputFileSuffix

        # Initialize the input file loader
        loader=inputFileLoader(inputFile, outputFile)
        loader.signals.finished.connect(self.loadingDone)

        # Start the snapshot loader
        self.loaderPool.start(loader)

        # Return
        return
    
    def loadingDone(self, fileDict: dict, propertyDict: dict, inputRootDir: str, outputFile: str) -> None:
        """
        Loading of a new file dictionary has been completed

        Parameters
        ----------
        fileDict : dict
            A dictionary with the information about the files of the galaxies to be classified
        propertyDict : dict
            A dictionary with previously determined properties of the galaxies to be classified
        inputRootDir : str
            The path to the root directory of the input file
        outputFile : str
            The path to the file to use for the writing of the properties of the galaxies
        """

        # Evaluate arguments
        self.inputRootDir=inputRootDir
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
        
        # Determine which galaxies have been classified
        self.__determineClassified()

        # Notify the window
        self.window.dictUpdated()

        # Enable actions
        self.actionSubstrate.setFileActionsEnabled(True)
        if(self.categoriesDict['categories']):
            self.actionSubstrate.setExclusionNavigationActionEnabled(True)

        # Return
        return
    
    def __determineClassified(self) -> None:
        """
        Determines which galaxies have been classified
        """

        # Get metadata
        ngalaxies=len(self.propertyDict['galaxies'])

        # Determine which galaxies have been classified
        self.classified=np.empty((ngalaxies,), dtype=bool)
        for igalaxy in range(ngalaxies):
            if(self.propertyDict['galaxies'][igalaxy]['categories']):
                self.classified[igalaxy]=True
            else:
                self.classified[igalaxy]=False

        # Return
        return
    
    def toggleExcludeClassified(self, enabled: bool) -> None:
        """
        Toggle the loading of only the unclassified galaxies
        """

        # Toggle the exclude classified flag
        self.excludeClassified=enabled

        # Trigger the exclusion of classified galaxes
        self.window.navigationToolbar.triggerClassifiedExclusion()

        # Check whether we need to load a new galaxy
        if(self.excludeClassified):
            # If the currently loaded galaxy is classified, load the next unclassified one
            if(self.window.igalaxy is not None):
                if(self.classified[self.window.igalaxy]):
                    self.switchGalaxy(1)
        else:
            # If no galaxy is currently loaded, load the first one
            if(self.window.igalaxy is None):
                self.window.loadGalaxy(0, noReadOut=True)

        # Return
        return
    
    def switchGalaxy(self, increment: int, noReadOut: bool = False) -> None:
        """
        Switch the currently loaded galaxy
        """

        # Switch galaxy
        if(self.window.igalaxy is not None):

            # Determine the effective increment

            if(self.excludeClassified):
                # Check whether there are no more galaxies to load
                if(np.all(self.classified)):
                    self.window.loadGalaxy(None, noReadOut=noReadOut)
                    return
                # Find the next unclassified galaxy
                ifirstUnclassified=self.window.igalaxy+increment
                while(True):
                    if(ifirstUnclassified==self.window.ngalaxies):
                        ifirstUnclassified=0
                    elif(ifirstUnclassified==-1):
                        ifirstUnclassified=self.window.ngalaxies-1
                    if(not self.classified[ifirstUnclassified]):
                        break
                    else:
                        ifirstUnclassified=ifirstUnclassified+increment
                incrementEffective=ifirstUnclassified-self.window.igalaxy
            else:
                incrementEffective=increment

            # Determine the index of the galaxy to be loaded
            igalaxy=self.window.igalaxy+incrementEffective
        
            # Evaluate the index of the galaxy
            if(igalaxy==self.window.ngalaxies):
                igalaxy=0
            elif(igalaxy==-1):
                igalaxy=self.window.ngalaxies-1
        
            # Load the galaxy
            self.window.loadGalaxy(igalaxy, noReadOut=noReadOut)

            # Check whether no galaxy should have been loaded
            if(self.excludeClassified):
                if(np.all(self.classified)):
                    self.window.loadGalaxy(None, noReadOut=noReadOut)

        # Return
        return
    
    def switchFilter(self, increment: int) -> None:
        """
        Switch the currently loaded filter
        """

        # Switch filter
        if(self.window.ifilter is not None):
            # Determine the index of the filter to be loaded
            ifilter=self.window.ifilter+increment
            # Evaluate the index of the filter
            if(ifilter==self.window.nfilters):
                ifilter=0
            elif(ifilter==-1):
                ifilter=self.window.nfilters-1
            # Load the filter
            self.window.loadFilter(ifilter)

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
        if(self.categoriesDict['categories']):
            self.propertyDict['galaxies'][igalaxy]['categories']=categories
        self.propertyDict['galaxies'][igalaxy]['comments']=comments

        # Write the property dictionary to file
        writeJSONFile(self.outputFile, self.propertyDict)

        # Determine whether the galaxy has been classified
        if(categories):
            self.classified[igalaxy]=True
        else:
            self.classified[igalaxy]=False

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
        action.setChecked(self.substrate.excludeClassified)
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

        # Return
        return
    
    def setExclusionNavigationActionEnabled(self, enabled: bool):
        """
        Enable/Disable the exclusion navigation action
        """

        # Enable/Disable the exclusion navigation action
        self.navigationActions[0].setEnabled(enabled)

        # Return
        return
    
    def setLoadNavigationActionsEnabled(self, enabled: bool):
        """
        Enable/Disable the load navigation actions
        """

        # Enable/Disable the load navigation actions
        for action in self.navigationActions[1:]:
            action.setEnabled(enabled)

        # Return
        return