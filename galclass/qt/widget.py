###########
# Imports #
###########

# System #

from typing import Optional

import os

from functools import partial

import numpy as np

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QKeySequence, QPixmap, QBrush, QPalette, QResizeEvent
from PyQt6.QtWidgets import QAbstractItemView, QCompleter, QSizePolicy, QComboBox, QLineEdit, QTableView, QMenuBar, QLabel, QWidget, QToolBar, QGridLayout, QGroupBox, QTextEdit, QCheckBox, QTabWidget, QToolButton, QSpacerItem
from PyQt6.QtPdfWidgets import QPdfView

# Local #

###########
# Classes #
###########

#**********#
# PDF view #
#**********#

class pdfView(QPdfView):
    """
    A widget for the viewing of PDF files
    """

    def __init__(self, parent: Optional[QWidget] = None):
        # Call super().__init__
        super().__init__(parent)
        # Initialize the pixmap
        self.pixmap=QPixmap(os.path.dirname(os.path.abspath(__file__))+'/../resources/mpe-mpa.png')
        # Return
        return

    def resizeEvent(self, event: Optional[QResizeEvent] = None) -> None:
        # Produce the scaled brush
        brush=QBrush(self.pixmap.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio))
        # Update the palette
        palette=self.palette()
        palette.setBrush(QPalette.ColorRole.Dark, brush)
        self.setPalette(palette)
        # Return
        return super().resizeEvent(event)

#**********#
# Menu bar #
#**********#

class MenuBar(QMenuBar):
    """
    A menu bar class with the action of the Qt action substrate
    """

    def __init__(self, parentWindow, substrate):
        """
        Constructor
        """

        # Evaluate arguments
        self.parentWindow=parentWindow
        self.substrate=substrate

        # Call super().__init__
        super().__init__()

        # Initialize file menu
        self.__initFileMenu()

        # Initialize view menu
        self.__initViewMenu()

        # Initialize navigation menu
        self.__initNavigationMenu()

        # Return
        return
    
    def __initFileMenu(self):
        """
        Initializes the "File" menu
        """

        # Add file menu
        self.fileMenu=self.addMenu("&File")

        # Add file actions
        self.fileMenu.addActions(self.substrate.actionSubstrate.fileActions[0:1])

        # Return
        return
    
    def __initViewMenu(self):
        """
        Initializes the "View" menu
        """

        # Add view menu
        self.viewMenu=self.addMenu("&View")

        # Add view actions
        self.viewMenu.addAction(self.parentWindow.navigationToolbar.toggleViewAction())
        self.viewMenu.addAction(self.parentWindow.infoToolbar.toggleViewAction())
        self.viewMenu.addAction(self.parentWindow.categoriesToolbar.toggleViewAction())

        # Return
        return
    
    def __initNavigationMenu(self):
        """
        Initializes the "Navigation" menu
        """

        # Add navigation menu
        self.navigationMenu=self.addMenu("&Navigation")

        # Add navigation actions

        # Add galaxy "Exclude Classified" action
        self.navigationMenu.addAction(self.substrate.actionSubstrate.navigationActions[0])

        # Add separator
        self.navigationMenu.addSeparator()

        # Add galaxy navigation actions
        self.navigationMenu.addActions(self.substrate.actionSubstrate.navigationActions[1:3])

        # Add separator
        self.navigationMenu.addSeparator()

        # Add filter navigation actions
        self.navigationMenu.addActions(self.substrate.actionSubstrate.navigationActions[3:5])

        # Return
        return

#**************#
# Info toolbar #
#**************#

class infoToolbar(QToolBar):
    """
    A toolbar class with information on each galaxy
    """

    def __init__(self, parentWindow, substrate):
        """
        Constructor
        """

        # Evaluate arguments
        self.parentWindow=parentWindow
        self.substrate=substrate

        # Call super().__init__
        super().__init__()

        # Set toolbar title and orientation
        self.setWindowTitle('Info Toolbar')
        self.setOrientation(Qt.Orientation.Vertical)

        # Initialize tabs
        self.__initInfoTab()
        
        # Initialize tab widget
        tabWidget=QTabWidget(self)
        tabWidget.addTab(self.infoTab, 'Info')

        # Add tab widget
        self.addWidget(tabWidget)

        # Return
        return
    
    def __initInfoTab(self):
        """
        Initialize the information tab
        """

        # Initialize the tab layout
        layout=QGridLayout()

        # Initialize the galaxy info group box
        galaxyInfoGroupbox=QGroupBox("Galaxy")
        galaxyInfoGroupbox.setCheckable(False)

        # Initialize the galaxy info groupbox layout
        galaxyInfoGroupboxLayout=QGridLayout()

        # Set column and row stretch
        galaxyInfoGroupboxLayout.setColumnStretch(0, 1)
        galaxyInfoGroupboxLayout.setRowStretch(0, 1)

        # Initialize the galaxy info model
        self.galaxyInfoModel=QStandardItemModel(self)
        self.galaxyInfoModel.setHorizontalHeaderLabels(["Key", "Value"])

        # Initialize the galaxy table view
        self.galaxyInfoTableView=QTableView(self)
        self.galaxyInfoTableView.setModel(self.galaxyInfoModel)
        self.galaxyInfoTableView.verticalHeader().setVisible(False)
        self.galaxyInfoTableView.horizontalHeader().setStretchLastSection(True)
        self.galaxyInfoTableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # Add the galaxy info table view
        galaxyInfoGroupboxLayout.addWidget(self.galaxyInfoTableView, 0, 0, 1, 1)

        # Set the galaxy info groupbox layout
        galaxyInfoGroupbox.setLayout(galaxyInfoGroupboxLayout)

        # Add the galaxy info groupbox to tab layout
        layout.addWidget(galaxyInfoGroupbox, 0, 0, 1, 1)

        # Initialize the filter info group box
        filterInfoGroupbox=QGroupBox("Filter")
        filterInfoGroupbox.setCheckable(False)

        # Initialize the filter info groupbox layout
        filterInfoGroupboxLayout=QGridLayout()

        # Set column and row stretch
        filterInfoGroupboxLayout.setColumnStretch(0, 1)
        filterInfoGroupboxLayout.setRowStretch(0, 1)

        # Initialize the filter info model
        self.filterInfoModel=QStandardItemModel(self)
        self.filterInfoModel.setHorizontalHeaderLabels(["Key", "Value"])

        # Initialize the filter table view
        self.filterInfoTableView=QTableView(self)
        self.filterInfoTableView.setModel(self.filterInfoModel)
        self.filterInfoTableView.verticalHeader().setVisible(False)
        self.filterInfoTableView.horizontalHeader().setStretchLastSection(True)
        self.filterInfoTableView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        # Add the filter info table view
        filterInfoGroupboxLayout.addWidget(self.filterInfoTableView, 0, 0, 1, 1)

        # Set the filter info groupbox layout
        filterInfoGroupbox.setLayout(filterInfoGroupboxLayout)

        # Add the filter info groupbox to tab layout
        layout.addWidget(filterInfoGroupbox, 1, 0, 1, 1)

        # Initialize info tab widget
        self.infoTab=QWidget()
        self.infoTab.setLayout(layout)

        # Return
        return
    
    def updateGalaxyInfoModel(self, info: dict):
        """
        Updates the items of the galaxy info model
        """

        # Clear the galaxy info model
        self.galaxyInfoModel.clear()

        # Add the info as items to the galaxy info model
        if(info):
            self.galaxyInfoModel.appendColumn([QStandardItem(str(key)) for key in info.keys()])
            self.galaxyInfoModel.appendColumn([QStandardItem(str(value)) for value in info.values()])
        
        # Set the horizontal header labels
        self.galaxyInfoModel.setHorizontalHeaderLabels(["Key", "Value"])

        # Return
        return
    
    def updateFilterInfoModel(self, info: dict):
        """
        Updates the items of the filter info model
        """

        # Clear the filter info model
        self.filterInfoModel.clear()

        # Add the info as items to the filter info model
        if(info):
            self.filterInfoModel.appendColumn([QStandardItem(str(key)) for key in info.keys()])
            self.filterInfoModel.appendColumn([QStandardItem(str(value)) for value in info.values()])
        
        # Set the horizontal header labels
        self.filterInfoModel.setHorizontalHeaderLabels(["Key", "Value"])

        # Return
        return

#********************#
# Categories toolbar #
#********************#

class categoriesToolbar(QToolBar):
    """
    A toolbar class with the classification options for each galaxy
    """

    def __init__(self, parentWindow, substrate):
        """
        Constructor
        """

        # Evaluate arguments
        self.parentWindow=parentWindow
        self.substrate=substrate

        # Initialize attributes
        self.categoryWidgetsEnabled=False

        # Call super().__init__
        super().__init__()

        # Set toolbar title and orientation
        self.setWindowTitle('Categories Toolbar')
        self.setOrientation(Qt.Orientation.Vertical)

        # Initialize tabs
        self.__initCategoriesTab()
        
        # Initialize tab widget
        tabWidget=QTabWidget(self)
        tabWidget.addTab(self.categoriesTab, 'Categories')

        # Add tab widget
        self.addWidget(tabWidget)

        # Return
        return
    
    def __buildCategoryTree(self, category: dict, depth: int = 1, isAlso: list = [], isNot: list = []):
        """
        Build the category tree of the specified category

        Parameters
        ----------
        category : str
            The dictionary of the category the tree of which to be built
        depth : int, optional
            The depth of the root of the tree (default is 1)
        isAlso : list, optional
            A list of categories of which the root category is a subcategory (default is [])
        isNot : list, optional
            A list of categories with which the root category is mutually exclusive (default is [])
        """

        # Initialize the checkboxes of all subcategories of the category

        for subcategory in category['categories']:

            # Determine the isAlso and isNot of the subcategory
            subname=subcategory['name']
            subisAlso=isAlso+subcategory['isAlso']
            subisNot=isNot+subcategory['isNot']

            # Initialize the checkbox of the subcategory
            checkbox=QCheckBox(self)
            checkbox.setCheckable(True)
            checkbox.setChecked(False)
            checkbox.setEnabled(self.categoryWidgetsEnabled)
            if(subcategory['shortcut']!=""):
                checkbox.setShortcut(QKeySequence(subcategory['shortcut']))
            checkbox.stateChanged.connect(partial(self.checkboxToggled, subname, subisAlso, subisNot))
            
            # Append the checkbox and its metadata to the category checkboxes list
            self.categoryCheckboxes['checkbox'].append(checkbox)
            self.categoryCheckboxes['name'].append(subname)
            self.categoryCheckboxes['isAlso'].append(subisAlso)
            self.categoryCheckboxes['isNot'].append(subisNot)
            self.categoryCheckboxes['depth'].append(depth)

            # Initialize the checkboxes of the subcategories of the subcategory
            self.__buildCategoryTree(subcategory, depth=depth+1, isAlso=subisAlso+[subname,], isNot=subisNot)

        # Return
        return
    
    def __initCategoriesTab(self):
        """
        Initialize the categories tab
        """

        # Initialize the category checkboxes dict
        self.categoryCheckboxes={'checkbox': [], 'name': [], 'isAlso': [], 'isNot': [], 'depth': []}

        # Build the category tree
        self.__buildCategoryTree(self.substrate.categoriesDict)

        # Determine the total number of categories
        self.ncategories=len(self.categoryCheckboxes['name'])

        # Determine the maximum depth of the category tree
        maxDepth=int(np.max(self.categoryCheckboxes['depth'], initial=0))

        # Initialize the tab layout
        layout=QGridLayout()

        # Check whether there are any categories available
        if(maxDepth>0):

            # Initialize the categories group box
            categoriesGroupbox=QGroupBox("Categories")
            categoriesGroupbox.setCheckable(False)

            # Initialize the categories groupbox layout
            categoriesGroupboxLayout=QGridLayout()

            # Set column stretch
            for idepth in range(maxDepth):
                categoriesGroupboxLayout.setColumnStretch(2*idepth, 0)
                categoriesGroupboxLayout.setColumnStretch(2*idepth+1, 1)
            categoriesGroupboxLayout.setColumnStretch(2*maxDepth, 1)
            
            # Add the categories labels and checkboxies
            for icategory in range(self.ncategories):
                # Add the label with the name of the category
                categoriesGroupboxLayout.addWidget(self.categoryCheckboxes['checkbox'][icategory], icategory, 2*(self.categoryCheckboxes['depth'][icategory]-1), Qt.AlignmentFlag.AlignLeft)
                # Add the checkbox of the category
                categoriesGroupboxLayout.addWidget(QLabel(self.categoryCheckboxes['name'][icategory]), icategory, 2*(self.categoryCheckboxes['depth'][icategory]-1)+1, Qt.AlignmentFlag.AlignLeft)

            # Add the horizontal spacer
            categoriesGroupboxLayout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding), 0, 2*maxDepth, self.ncategories, 1)

            # Set the categories groupbox layout
            categoriesGroupbox.setLayout(categoriesGroupboxLayout)

            # Add the categories groupbox to tab layout
            layout.addWidget(categoriesGroupbox, 0, 0, 1, 1)

        # Initialize the comments group box
        commentsGroupbox=QGroupBox("Comments")
        commentsGroupbox.setCheckable(False)

        # Initialize the comments groupbox layout
        commentsGroupboxLayout=QGridLayout()

        # Set column and row stretch
        commentsGroupboxLayout.setColumnStretch(0, 1)
        commentsGroupboxLayout.setRowStretch(0, 1)
        
        # Add the comments text edit
        self.commentsTextEdit=QTextEdit("", self)
        self.commentsTextEdit.setEnabled(self.categoryWidgetsEnabled)
        commentsGroupboxLayout.addWidget(self.commentsTextEdit, 0, 0)

        # Set the comments groupbox layout
        commentsGroupbox.setLayout(commentsGroupboxLayout)

        # Add the comments groupbox to tab layout
        layout.addWidget(commentsGroupbox, 1, 0, 1, 1)

        # Initialize categories tab widget
        self.categoriesTab=QWidget()
        self.categoriesTab.setLayout(layout)

        # Return
        return
    
    def checkboxToggled(self, name: str, isAlso: list, isNot: list, checked: bool):
        """
        Handles the toggling of a checkbox

        Parameters
        ----------
        name : str
            The name of the category of the toggled checkbox
        isAlso : list
            A list of categories of which the category of the toggled checkbox is a subcategory
        isNot : list, optional
            A list of categories with which the category of the toggled checkbox is mutually exclusive
        """

        # Get checkbox toggled

        for icategory in range(self.ncategories):

            # Determine the metadata of the category
            subcheckbox=self.categoryCheckboxes['checkbox'][icategory]
            subname=self.categoryCheckboxes['name'][icategory]
            subisAlso=self.categoryCheckboxes['isAlso'][icategory]
            subisNot=self.categoryCheckboxes['isNot'][icategory]

            # Determine whether the checkbox needs to be toggled or not
            if(checked):
                if(subname in isAlso):
                    subcheckbox.setChecked(True)
                if(subname in isNot):
                    subcheckbox.setChecked(False)
            else:
                if(name in subisAlso):
                    subcheckbox.setChecked(False)

        # Return
        return
    
    def readOut(self) -> list:
        """
        Reads the categories toolbar items and determines the categories and comments of the galaxy
        """

        # Determine the categories of which the galaxy is a part
        categories=[]
        for icategory in range(self.ncategories):
            if(self.categoryCheckboxes['checkbox'][icategory].isChecked()):
                categories.append(self.categoryCheckboxes['name'][icategory])
        
        # Determine the comments for the galaxy
        comments=self.commentsTextEdit.toPlainText()

        # Return
        return [categories, comments]
    
    def toggleCategoryWidgets(self, enabled: bool):
        """
        Enable/Disable the category widgets
        """

        # Evaluate arguments
        self.categoryWidgetsEnabled=enabled

        # Enable/Disable the category checkboxes
        for icategory in range(self.ncategories):
            self.categoryCheckboxes['checkbox'][icategory].setEnabled(enabled)
        
        # Enable/Disable the comments textedit
        self.commentsTextEdit.setEnabled(enabled)

        # Return
        return
    
    def clear(self, categories: list = [], comments: str = "") -> None:
        """
        Clears the categories tab with the specified properties

        Parameters
        ----------
        categories : list, optional
            The categories to be checked (default is [])
        comments : list, optional
            The comments to be displayed (default is "")
        """
        
        # Check the checkboxes that correspond to the specified catergories and uncheck everything else
        for icategory in range(self.ncategories):
            self.categoryCheckboxes['checkbox'][icategory].blockSignals(True)
            if(self.categoryCheckboxes['name'][icategory] in categories):
                self.categoryCheckboxes['checkbox'][icategory].setChecked(True)
            else:
                self.categoryCheckboxes['checkbox'][icategory].setChecked(False)
            self.categoryCheckboxes['checkbox'][icategory].blockSignals(False)
        
        # Restore the comments in the comments textedit
        self.commentsTextEdit.setText(comments)

        # Return
        return

#********************#
# Navigation toolbar #
#********************#

class navigationToolbar(QToolBar):
    """
    A toolbar class with navigation options for each galaxy / galaxy sample
    """

    def __init__(self, parentWindow, substrate):
        """
        Constructor
        """

        # Evaluate arguments
        self.parentWindow=parentWindow
        self.substrate=substrate

        # Call super().__init__
        super().__init__()

        # Set toolbar title and orientation
        self.setWindowTitle('Navigation Toolbar')
        self.setOrientation(Qt.Orientation.Horizontal)

        # Initialize tabs
        self.__initNavigationTab()

        # Initialize tab widget
        tabWidget=QTabWidget(self)
        tabWidget.addTab(self.navigationTab, 'Navigation')

        # Add tab widget
        self.addWidget(tabWidget)

        # Return
        return
    
    def __initNavigationTab(self):
        """
        Initialize the navigation tab
        """

        # Initialize the tab layout
        layout=QGridLayout()

        # Initialize the galaxy group box
        galaxyGroupbox=QGroupBox("Galaxy")
        galaxyGroupbox.setCheckable(False)

        # Initialize the galaxy layout
        galaxyGroupboxLayout=QGridLayout()

        # Set row stretch
        galaxyGroupboxLayout.setRowStretch(0, 1)
        galaxyGroupboxLayout.setRowStretch(1, 1)
        galaxyGroupboxLayout.setRowStretch(2, 1)
        galaxyGroupboxLayout.setRowStretch(3, 1)

        # Initialize the galaxy groupbox widgets

        # Initialize the previous galaxy button
        self.previousGalaxyButton=QToolButton(self)
        self.previousGalaxyButton.setDefaultAction(self.substrate.actionSubstrate.navigationActions[1])

        # Initialize the galaxy combobox
        self.galaxyCombobox=QComboBox(self)
        self.galaxyCombobox.setEditable(False)
        self.galaxyCombobox.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.galaxyCombobox.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.galaxyCombobox.currentIndexChanged.connect(self.parentWindow.loadGalaxy)

        # Initialize the galaxy model and completer
        self.galaxyModel=QStandardItemModel(self)
        self.galaxyCompleter=QCompleter()
        self.galaxyCompleter.setModel(self.galaxyModel)
        self.galaxyCompleter.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.galaxyCompleter.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.galaxyCompleter.activated.connect(self.performGalaxySearch)

        # Initialize the galaxy line edit
        self.galaxyLineEdit=QLineEdit(self)
        self.galaxyLineEdit.setPlaceholderText("Search")
        self.galaxyLineEdit.setCompleter(self.galaxyCompleter)
        self.galaxyLineEdit.editingFinished.connect(self.performGalaxySearch)

        # Initialize the next galaxy button
        self.nextGalaxyButton=QToolButton(self)
        self.nextGalaxyButton.setDefaultAction(self.substrate.actionSubstrate.navigationActions[2])

        # Append the galaxy widgets to the layout
        galaxyGroupboxLayout.addWidget(self.previousGalaxyButton, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        galaxyGroupboxLayout.addWidget(self.galaxyCombobox, 0, 1, 1, 1, Qt.AlignmentFlag.AlignHCenter)
        galaxyGroupboxLayout.addWidget(self.galaxyLineEdit, 0, 2, 1, 1, Qt.AlignmentFlag.AlignHCenter)
        galaxyGroupboxLayout.addWidget(self.nextGalaxyButton, 0, 3, 1, 1, Qt.AlignmentFlag.AlignRight)

        # Set the galaxy groupbox layout
        galaxyGroupbox.setLayout(galaxyGroupboxLayout)

        # Add the galaxy groupbox to tab layout
        layout.addWidget(galaxyGroupbox, 0, 0, 1, 1)

        # Initialize the filter group box
        filterGroupbox=QGroupBox("Filter")
        filterGroupbox.setCheckable(False)

        # Initialize the filter layout
        filterGroupboxLayout=QGridLayout()

        # Set row stretch
        filterGroupboxLayout.setRowStretch(0, 1)
        filterGroupboxLayout.setRowStretch(1, 1)
        filterGroupboxLayout.setRowStretch(2, 1)

        # Initialize the filter groubox widgets

        # Initialize the previous filter button
        self.previousFilterButton=QToolButton(self)
        self.previousFilterButton.setDefaultAction(self.substrate.actionSubstrate.navigationActions[3])

        # Initialize the filter combobox
        self.filterCombobox=QComboBox(self)
        self.filterCombobox.setEditable(False)
        self.filterCombobox.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.filterCombobox.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.filterCombobox.currentIndexChanged.connect(self.parentWindow.loadFilter)

        # Initialize the next filter button
        self.nextFilterButton=QToolButton(self)
        self.nextFilterButton.setDefaultAction(self.substrate.actionSubstrate.navigationActions[4])

        # Append the filter widgets to the layout
        filterGroupboxLayout.addWidget(self.previousFilterButton, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        filterGroupboxLayout.addWidget(self.filterCombobox, 0, 1, 1, 1, Qt.AlignmentFlag.AlignHCenter)
        filterGroupboxLayout.addWidget(self.nextFilterButton, 0, 2, 1, 1, Qt.AlignmentFlag.AlignRight)

        # Set the filter groupbox layout
        filterGroupbox.setLayout(filterGroupboxLayout)

        # Add the filter groupbox to tab layout
        layout.addWidget(filterGroupbox, 0, 1, 1, 1)

        # Initialize the navigation tab widget
        self.navigationTab=QWidget()
        self.navigationTab.setLayout(layout)

        # Return
        return
    
    def triggerClassifiedExclusion(self):
        """
        Triggers the exclusion of classified galaxies
        """

        if(self.substrate.excludeClassified):
            # Enable the unclassified galaxies and disbale the classified ones
            for igalaxy in range(self.parentWindow.ngalaxies):
                self.galaxyCombobox.model().item(igalaxy).setEnabled(not self.substrate.classified[igalaxy])
        else:
            # Enable all galaxies
            for igalaxy in range(self.parentWindow.ngalaxies):
                self.galaxyCombobox.model().item(igalaxy).setEnabled(True)

        # Return
        return
    
    def triggerGalaxyExclusion(self, igalaxy: int):
        """
        Trigger the exclusion of the specified galaxy

        Parameters
        ----------
        igalaxy : int
            The ID of the galaxy the exclusion of which is to be triggered
        """

        # Trigger the exclusion of the galaxy
        if(self.substrate.excludeClassified):
            self.galaxyCombobox.model().item(igalaxy).setEnabled(not self.substrate.classified[igalaxy])

        # Return
        return
    
    def performGalaxySearch(self):
        """
        Performs the search for the galaxy specified in the galaxy line edit
        """

        # Search for a galaxy with the specified name
        igalaxy=self.galaxyCombobox.findText(self.galaxyLineEdit.text(), Qt.MatchFlag.MatchFixedString)

        # If a galaxy is found, load it
        if(igalaxy>=0):
            self.parentWindow.loadGalaxy(igalaxy)

        # Clear the galaxy line edit
        QTimer.singleShot(0, self.galaxyLineEdit.clear)

        # Return
        return
    
    def updateGalaxyModel(self, galaxies: list):
        """
        Updates the items of the model to be used for autocompletion
        """

        # Clear the galaxy model
        self.galaxyModel.clear()

        # Add the galaxies as items to the galaxy model
        for galaxy in galaxies:
            self.galaxyModel.appendRow(QStandardItem(galaxy))

        # Return
        return
    
    def updateGalaxyCombobox(self, galaxies: list):
        """
        Updates the entries of the galaxy combobox
        """

        # Suppress the signals of the galaxy combobox
        self.galaxyCombobox.blockSignals(True)

        # Update the entries of the galaxy combobox
        self.galaxyCombobox.clear()
        self.galaxyCombobox.addItems(galaxies)

        # Select the first entry of the galaxy combobox
        self.galaxyCombobox.setCurrentIndex(0)

        # Stop suppressing the signals of the galaxy combobox
        self.galaxyCombobox.blockSignals(False)

        # Return
        return
    
    def updateFilterCombobox(self, filters: list):
        """
        Updates the entries of the filter combobox
        """

        # Suppress the signals of the filter combobox
        self.filterCombobox.blockSignals(True)

        # Update the entries of the filter combobox
        self.filterCombobox.clear()
        self.filterCombobox.addItems(filters)

        # Select the first entry of the filters combobox
        self.filterCombobox.setCurrentIndex(0)

        # Stop suppressing the signals of the filters combobox
        self.filterCombobox.blockSignals(False)

        # Return
        return