###########
# Imports #
###########

# System #

from typing import Optional

import os

import numpy as np

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QKeyEvent, QCloseEvent, QKeySequence
from PyQt6.QtWidgets import QMainWindow, QLayout, QHBoxLayout, QWidget, QStatusBar
from PyQt6.QtPdf import QPdfDocument
from PyQt6.QtPdfWidgets import QPdfView

# Local #

from .widget import pdfView, MenuBar, navigationToolbar, infoToolbar, categoriesToolbar

###########
# Classes #
###########

#*************#
# Main window #
#*************#

class MainWindow(QMainWindow):
    """
    The class of the main window of the application
    """

    def __init__(self, substrate):
        """
        Constructor
        """

        # Evaluate arguments
        self.substrate=substrate

        # Initialize attributes
        self.ngalaxies=0
        self.igalaxy=None
        self.nfilters=0
        self.ifilter=None

        # Call super().__init__
        super().__init__()

        # Set window title
        self.__updateWindowTitle()

        # Set minimum size
        self.setMinimumSize(QSize(1024, 768))

        # Initialize layout
        layout=QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Initialize dummy QWidget
        widget=QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Initialize the pdf view
        self.__initPdfView(layout)

        # Initialize toolbars
        self.__initToolbars()
        
        # Initialize status bar
        # self.statusBar=QStatusBar(self)
        # self.setStatusBar(self.statusBar)

        # Initialize menu bar
        self.menuBar=MenuBar(self, self.substrate)
        self.setMenuBar(self.menuBar)

        # Set drop policy
        self.setAcceptDrops(True)

        # Return
        return
    
    def __initPdfView(self, layout: QLayout):
        """
        Initializes the Qt PDF View
        """

        # Initialize the pdf document
        self.pdfDocument=QPdfDocument(self)

        # Initialize the pdf view
        self.pdfView=pdfView(self)
        self.pdfView.setDocument(self.pdfDocument)
        self.pdfView.setZoomMode(QPdfView.ZoomMode.FitInView)
        self.pdfView.setPageMode(QPdfView.PageMode.SinglePage)

        # Load no pdf document
        self.pdfDocument.load(None)
    
        # Add the pdf view to the layout
        layout.addWidget(self.pdfView)

        # Return
        return
    
    def __initToolbars(self):
        """
        Initialize the toolbars of the window
        """

        # Initialize the toolbars
        self.navigationToolbar=navigationToolbar(self, self.substrate)
        self.infoToolbar=infoToolbar(self, self.substrate)
        self.categoriesToolbar=categoriesToolbar(self, self.substrate)
        
        # Add toggle toolbar shortcuts
        # self.navigationToolbar.toggleViewAction().setShortcut(QKeySequence('Ctrl+n'))
        # self.infoToolbar.toggleViewAction().setShortcut(QKeySequence('Ctrl+i'))
        # self.categoriesToolbar.toggleViewAction().setShortcut(QKeySequence('Ctrl+c'))
        
        # Attach the toolbars
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.navigationToolbar)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.infoToolbar)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.categoriesToolbar)
        
        # Show toolbars
        self.navigationToolbar.show()
        self.infoToolbar.show()
        self.categoriesToolbar.show()
        
        # Return
        return
    
    def __updateWindowTitle(self) -> None:
        """
        Updates the title of the window
        """

        # Determine the title of the window
        windowTitle="galclass"
        if((self.substrate.categoriesDict['categories'])and(self.substrate.classified is not None)):
            windowTitle=windowTitle+' '
            windowTitle=windowTitle+'('
            windowTitle=windowTitle+str(np.sum(self.substrate.classified, dtype=int))
            windowTitle=windowTitle+'/'
            windowTitle=windowTitle+str(self.substrate.classified.shape[0])
            windowTitle=windowTitle+')'

        # Set window title
        self.setWindowTitle(windowTitle)

        # Return
        return
    
    def dictUpdated(self) -> None:
        """
        The file dictionary of the Qt substrate has been updated
        """

        # Update the metadata of the files
        self.ngalaxies=len(self.substrate.fileDict['galaxies'])

        # Update the galaxy combobox
        self.navigationToolbar.updateGalaxyCombobox([self.substrate.fileDict['galaxies'][igalaxy]['name'] for igalaxy in range(self.ngalaxies)])

        # Update the galaxy model
        self.navigationToolbar.updateGalaxyModel([self.substrate.fileDict['galaxies'][igalaxy]['name'] for igalaxy in range(self.ngalaxies)])

        # Trigger the exclusion of classified galaxies
        self.navigationToolbar.triggerClassifiedExclusion()

        # Update the title of the windows
        self.__updateWindowTitle()

        # Load the first galaxy of the file dictionary
        self.loadGalaxy(self.ngalaxies-1, noReadOut=True)
        self.substrate.switchGalaxy(1, noReadOut=True)

        # Return
        return
    
    def loadGalaxy(self, igalaxy: Optional[int] = None, noReadOut: bool = False):
        """
        Load the galaxy with the specified ID

        Parameters
        ----------
        igalaxy : int, optional
            The ID of the galaxy to load (default is None)
        noReadOut : bool, optional
            Should we skip the reading out of the properties of the current galaxy? (default is False)
        """

        # Read out the properties of the current galaxy
        if(not noReadOut):
            if(self.igalaxy is not None):
                self.substrate.updateGalaxyProperties(self.igalaxy, *self.categoriesToolbar.readOut())
                self.navigationToolbar.triggerGalaxyExclusion(self.igalaxy)
                self.__updateWindowTitle()
        
        # Check whether no galaxy is to be loaded

        if(igalaxy is None):

            # Disable navigation and category controls
            if(self.igalaxy is not None):
                # Disable the navigation actions
                self.substrate.actionSubstrate.setLoadNavigationActionsEnabled(False)
                # Disable the category widgets
                self.categoriesToolbar.toggleCategoryWidgets(False)

            # Update the current galaxy ID
            self.igalaxy=igalaxy
            self.nfilters=0

            # Clear the categories checkboxes
            self.categoriesToolbar.clear()

            # Clear the current index of the galaxy combobox
            self.navigationToolbar.galaxyCombobox.blockSignals(True)
            self.navigationToolbar.galaxyCombobox.setCurrentIndex(-1)
            self.navigationToolbar.galaxyCombobox.blockSignals(False)

            # Clear the galaxy info model
            self.infoToolbar.updateGalaxyInfoModel({})

            # Clear the filter combobox
            self.navigationToolbar.updateFilterCombobox({})

            # Load no filter
            self.loadFilter(None)
        
        else:

            # Enable navigation and category controls
            if(self.igalaxy is None):
                # Enable the navigation actions
                self.substrate.actionSubstrate.setLoadNavigationActionsEnabled(True)
                # Enable the category widgets
                self.categoriesToolbar.toggleCategoryWidgets(True)

            # Update the current galaxy ID
            self.igalaxy=igalaxy
            self.nfilters=len(self.substrate.fileDict['galaxies'][self.igalaxy]['filters'])

            # Clear the categories checkboxes
            self.categoriesToolbar.clear(categories=self.substrate.propertyDict['galaxies'][self.igalaxy]['categories'], comments=self.substrate.propertyDict['galaxies'][self.igalaxy]['comments'])

            # Set the current index of the galaxy combobox
            self.navigationToolbar.galaxyCombobox.blockSignals(True)
            self.navigationToolbar.galaxyCombobox.setCurrentIndex(self.igalaxy)
            self.navigationToolbar.galaxyCombobox.blockSignals(False)

            # Update the galaxy info model
            galaxyInfo={"Name": self.substrate.fileDict['galaxies'][self.igalaxy]['name'], "Filters": self.substrate.fileDict['galaxies'][self.igalaxy]['filters']}
            galaxyInfo.update(self.substrate.fileDict['galaxies'][self.igalaxy]['info'])
            self.infoToolbar.updateGalaxyInfoModel(galaxyInfo)

            # Update the filter combobox
            self.navigationToolbar.updateFilterCombobox(self.substrate.fileDict['galaxies'][self.igalaxy]['filters'])

            # Load the first filter of the galaxy
            self.loadFilter(0)

        # Return
        return
    
    def loadFilter(self, ifilter: Optional[int] = None):
        """
        Load the filter with the specified ID

        Parameters
        ----------
        ifilter : int, optional
            The ID of the filter to load (default is None)
        """

        # Update the current filter ID
        self.ifilter=ifilter

        # Check whether no filter is to be loaded

        if(ifilter is None):

            # Clear the current index of the filter combobox
            self.navigationToolbar.filterCombobox.blockSignals(True)
            self.navigationToolbar.filterCombobox.setCurrentIndex(-1)
            self.navigationToolbar.filterCombobox.blockSignals(False)

            # Clear the filter info model
            self.infoToolbar.updateFilterInfoModel({})

            # Load no pdf document
            self.pdfDocument.load(None)

        else:

            # Set the current index of the filter combobox
            self.navigationToolbar.filterCombobox.blockSignals(True)
            self.navigationToolbar.filterCombobox.setCurrentIndex(self.ifilter)
            self.navigationToolbar.filterCombobox.blockSignals(False)

            # Update the filter info model
            filterInfo={"Name": self.substrate.fileDict['galaxies'][self.igalaxy]['filters'][self.ifilter]}
            filterInfo.update(self.substrate.fileDict['galaxies'][self.igalaxy]['fileInfo'][self.ifilter])
            self.infoToolbar.updateFilterInfoModel(filterInfo)

            # Determine the path to the filter pdf file
            filePath=os.path.abspath(os.path.join(self.substrate.inputRootDir, self.substrate.fileDict['galaxies'][self.igalaxy]['files'][self.ifilter]))

            # Load the filter pdf in the pdf view
            self.pdfDocument.load(filePath)
        
        # Set the focus to the pdf view
        self.pdfView.setFocus()

        # Return
        return
    
    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Closes the window

        Parameters
        ----------
        event : QCloseEvent
            The close event
        """

        # Read out the properties of the current galaxy
        if(self.categoriesToolbar.categoryWidgetsEnabled):
            self.substrate.updateGalaxyProperties(self.igalaxy, *self.categoriesToolbar.readOut())

        # Close the main window
        self.substrate.closeMainWindow()

        # Call super().closeEvent
        super().closeEvent(event)
        
        # Return
        return
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Evaluates a key press to check whether the window should be closed

        Parameters
        ----------
        event : QKeyEvent
            The key event to evaluate
        """

        # Evaluate key press
        if((event.key()==Qt.Key.Key_W)and(event.modifiers() & Qt.KeyboardModifier.ControlModifier)):
            # Trigger the close event
            self.closeEvent(QCloseEvent())

        # Return
        return
    
    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """
        Accepts a drag event if it contains URLs and rejects it otherwise

        Parameters
        ----------
        event : QDragEnterEvent
            The drag event to evaluate
        """

        # Accept only URLs
        if(event.mimeData().hasUrls()):
            event.accept()
        else:
            event.ignore()
        
        # Return
        return

    def dropEvent(self, event: QDropEvent) -> None:
        """
        Evaluates a drop event by opening the first URLs it contains

        Parameters
        ----------
        event : QDropEvent
            The drop event to evaluate
        """

        # Determine file paths
        fileList=[]
        for url in event.mimeData().urls():
            fileList.append(url.toLocalFile())
        
        # Call the file drop handler function of the Qt substrate
        self.substrate.openInputFile(fileList[0])
        
        # Return
        return

    def updateStatusBarMessage(self, message: str):

        # Update the status bar message
        # self.statusBar.showMessage(message)

        # Return
        return