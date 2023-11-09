###########
# Imports #
###########

# System #

from typing import Optional

import os

from PyQt6.QtCore import QSize, Qt, QUrl
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QKeyEvent, QCloseEvent, QKeySequence
from PyQt6.QtWidgets import QMainWindow, QLayout, QHBoxLayout, QWidget, QStatusBar
from PyQt6.QtWebEngineWidgets import QWebEngineView

# Local #

from .widget import MenuBar, navigationToolbar, categoriesToolbar

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
        self.igalaxy=0
        self.nfilters=0
        self.ifilter=0

        # Call super().__init__
        super().__init__()

        # Set window title
        self.setWindowTitle("galclass")

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

        # Initialize the web view
        self.__initWebView(layout=layout)

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
    
    def __initWebView(self, layout: Optional[QLayout] = None):
        """
        Initializes the Qt Web View Engine and sets 
        """

        # Initialize the web view
        self.webView=QWebEngineView()
        # self.webView.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, False)
        self.webView.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.webView.settings().setAttribute(self.webView.settings().WebAttribute.NavigateOnDropEnabled, False)
        self.webView.settings().setAttribute(self.webView.settings().WebAttribute.NavigateOnDropEnabled, False)
        self.webView.settings().setAttribute(self.webView.settings().WebAttribute.NavigateOnDropEnabled, False)
        self.webView.settings().setAttribute(self.webView.settings().WebAttribute.PluginsEnabled, True)
        self.webView.settings().setAttribute(self.webView.settings().WebAttribute.PdfViewerEnabled, True)

        # Set the default page of the web view
        self.defaultHtml="""
        <html>
            <head>
                <style>
                    html {
                        background: url("BACKGROUND_IMAGE_PATH") no-repeat center center fixed;
                        -webkit-background-size: cover;
                        -moz-background-size: cover;
                        -o-background-size: cover;
                        background-size: cover;
                        background-color: #000000;
                    }
                </style>
            </head>
            <body></body>
        </html>
        """
        self.defaultHtml=self.defaultHtml.replace("BACKGROUND_IMAGE_PATH", 'file://'+os.path.dirname(os.path.abspath(__file__))+'/../resources/mpe-mpa.png')
        self.webView.setHtml(self.defaultHtml, baseUrl=QUrl('file://'))
    
        # Add the web view to the layout
        layout.addWidget(self.webView)

        # Return
        return
    
    def __initToolbars(self):
        """
        Initialize the toolbars of the window
        """

        # Initialize the toolbars
        self.categoriesToolbar=categoriesToolbar(self, self.substrate)
        self.navigationToolbar=navigationToolbar(self, self.substrate)
        
        # Add toggle toolbar shortcut
        # self.categoriesToolbar.toggleViewAction().setShortcut(QKeySequence('Ctrl+C'))
        
        # Attach the toolbars
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.categoriesToolbar)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.navigationToolbar)
        # self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.snapToolbar)
        
        # Show toolbars
        self.categoriesToolbar.show()
        self.navigationToolbar.show()
        
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

        # Load the first galaxy of the file dictionary
        self.loadGalaxy(0, noReadOut=True)

        # Return
        return
    
    def loadGalaxy(self, igalaxy: int, noReadOut: bool = False):
        """
        Load the galaxy with the specified ID

        Parameters
        ----------
        igalaxy : int
            The ID of the galaxy to load
        noReadOut : bool, optional
            Should we skip the reading out of the properties of the current galaxy? (default is False)
        """

        # Read out the properties of the current galaxy
        if(not noReadOut):
            self.substrate.updateGalaxyProperties(self.igalaxy, *self.categoriesToolbar.readOut())

        # Evaluate the galaxy ID
        if(self.ngalaxies==0):
            return
        elif(igalaxy==self.ngalaxies):
            igalaxy=0
        elif(igalaxy==-1):
            igalaxy=self.ngalaxies-1

        # Update the current galaxy ID
        self.igalaxy=igalaxy
        self.nfilters=len(self.substrate.fileDict['galaxies'][self.igalaxy]['filters'])

        # Clear the categories checkboxes
        self.categoriesToolbar.clear(categories=self.substrate.propertyDict['galaxies'][self.igalaxy]['categories'], comments=self.substrate.propertyDict['galaxies'][self.igalaxy]['comments'])

        # Set the current index of the galaxy combobox
        self.navigationToolbar.galaxyCombobox.blockSignals(True)
        self.navigationToolbar.galaxyCombobox.setCurrentIndex(self.igalaxy)
        self.navigationToolbar.galaxyCombobox.blockSignals(False)

        # Update the info model
        infoOfGalaxy={"Name": self.substrate.fileDict['galaxies'][self.igalaxy]['name'], "Filters": self.substrate.fileDict['galaxies'][self.igalaxy]['filters']}
        # infoOfGalaxy.update(self.substrate.fileDict['galaxies'][self.igalaxy]['info'])
        self.categoriesToolbar.updateInfoModel(infoOfGalaxy)

        # Update the filter combobox
        self.navigationToolbar.updateFilterCombobox(self.substrate.fileDict['galaxies'][self.igalaxy]['filters'])

        # Load the first filter of the galaxy
        self.loadFilter(0)

        # Return
        return
    
    def loadFilter(self, ifilter: int):
        """
        Load the filter with the specified ID

        Parameters
        ----------
        ifilter : int
            The ID of the filter to load
        """

        # Evaluate the filter ID
        if(self.nfilters==0):
            return
        elif(ifilter==self.nfilters):
            ifilter=0
        elif(ifilter==-1):
            ifilter=self.nfilters-1

        # Update the current filter ID
        self.ifilter=ifilter

        # Set the current index of the filter combobox
        self.navigationToolbar.filterCombobox.blockSignals(True)
        self.navigationToolbar.filterCombobox.setCurrentIndex(self.ifilter)
        self.navigationToolbar.filterCombobox.blockSignals(False)

        # Determine the path to the filter pdf file
        filePath=os.path.abspath(self.substrate.fileDict['galaxies'][self.igalaxy]['files'][self.ifilter])

        # Load the filter pdf in the web view
        self.webView.setUrl(QUrl("file://"+filePath.replace('\\', '/')))

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