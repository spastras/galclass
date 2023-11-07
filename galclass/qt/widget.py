###########
# Imports #
###########

# System #

import numpy as np

from functools import partial

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSizePolicy, QComboBox, QMenuBar, QLabel, QWidget, QToolBar, QGridLayout, QGroupBox, QTextEdit, QCheckBox, QTabWidget, QToolButton, QSpacerItem

# Local #

###########
# Classes #
###########

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
        maxDepth=np.max(self.categoryCheckboxes['depth'])

        # Initialize the tab layout
        layout=QGridLayout()

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
        commentsGroupbox=QGroupBox("Commnets")
        commentsGroupbox.setCheckable(False)

        # Initialize the comments groupbox layout
        commentsGroupboxLayout=QGridLayout()

        # Set column and row stretch
        commentsGroupboxLayout.setColumnStretch(0, 1)
        commentsGroupboxLayout.setRowStretch(0, 1)
        
        # Add the comments text edit
        self.commentsTextEdit=QTextEdit("", self)
        self.commentsTextEdit.setEnabled(self.categoryWidgetsEnabled)
        commentsGroupboxLayout.addWidget(self.commentsTextEdit, 0, 0, Qt.AlignmentFlag.AlignLeft)

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
        
        # Determine the commnets for the galaxy
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

        # Initialize the next galaxy button
        self.nextGalaxyButton=QToolButton(self)
        self.nextGalaxyButton.setDefaultAction(self.substrate.actionSubstrate.navigationActions[2])

        # Append the galaxy widgets to the layout
        galaxyGroupboxLayout.addWidget(self.previousGalaxyButton, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        galaxyGroupboxLayout.addWidget(self.galaxyCombobox, 0, 1, 1, 1, Qt.AlignmentFlag.AlignHCenter)
        galaxyGroupboxLayout.addWidget(self.nextGalaxyButton, 0, 2, 1, 1, Qt.AlignmentFlag.AlignRight)

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