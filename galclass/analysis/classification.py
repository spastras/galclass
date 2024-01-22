###########
# Imports #
###########

# System #

from __future__ import annotations

from _collections_abc import Iterable

from typing import Optional, Union

import numpy as np

# Local #

from ..fileio import readJSONFile

###########
# Classes #
###########

#****************#
# Classification #
#****************#

class classification():
    """
    A class for the handling of a classification of a sample
    """

    def __init__(self, items: Iterable, itemCategories: Iterable, itemComments: Iterable, categories: Iterable) -> None:
        """
        Constructor
        """

        # Evaluate arguments
        self.items=items
        self.itemCategories=itemCategories
        self.itemComments=itemComments
        self.categories=categories

        # Get metadata
        self.nitems=len(items)

        # Return
        return
    
    def __getItemID(self, item: str):
        """
        Return the ID of the specified item

        Parameters
        ----------
        item : str
            The item the ID of which to return
        """

        # Determine the item id of the specified item
        itemID=-1
        for iitem in range(self.nitems):
            if(self.items[iitem]==item):
                itemID=iitem
                break
        
        # Make sure that the item has beeen found
        assert (itemID!=-1), "the specified item is not part of this classification"
        
        # Return
        return itemID
    
    def __getCategoryID(self, category: str):
        """
        Return the ID of the specified category

        Parameters
        ----------
        category : str
            The category the ID of which to return
        """

        # Determine the item id of the specified category
        categoryID=-1
        for icategory in range(self.ncategories):
            if(self.categories[icategory]==category):
                categoryID=icategory
                break
        
        # Make sure that the category has beeen found
        assert (categoryID!=-1), "the specified category is not part of this combined classification"
        
        # Return
        return categoryID
    
    def getCategoriesOf(self, item: str) -> list:
        """
        Return the categories of the specified item

        Parameters
        ----------
        item : str
            The item the categories of which to return
        """

        # Return
        return self.itemCategories[self.__getItemID(item)]
    
    def getCommentsOn(self, item: str) -> list:
        """
        Return the comments on the specified item

        Parameters
        ----------
        item : str
            The item the comments on which to return
        """

        # Return
        return self.itemComments[self.__getItemID(item)]
    
    def getNumberOf(self, category: str) -> int:
        """
        Determine the number of items in the specified category

        Parameters
        ----------
        category : str
            The category the number of items in which to determine
        """

        # Evaluate arguments
        assert (category in self.categories), "the requested category is not present"

        # Determine the number of items in this category
        nitemsInCategory=0
        for iitem in range(self.nitems):
            if(category in self.itemCategories[iitem]):
                nitemsInCategory=nitemsInCategory+1

        # Return
        return nitemsInCategory

    def getFractionOf(self, category: str) -> float:
        """
        Determines the fraction of items in the specified category

        Parameters
        ----------
        category : str
            The category the fraction of items in which to determine
        """

        # Return
        return float(self.getNumberOf(category)/self.nitems)

    def getItemsIn(self, category: str) -> list:
        """
        Return the items in the specified category

        Parameters
        ----------
        category : str
            The category the items in which to return
        """

        # Evaluate arguments
        assert (category in self.categories), "the requested category is not present"

        # Determine the number of items in this category
        itemsInCategory=[]
        for iitem in range(self.nitems):
            if(category in self.itemCategories[iitem]):
                itemsInCategory.append(itemsInCategory)

        # Return
        return itemsInCategory

#*************************#
# Combined classification #
#*************************#

class combinedClassification(classification):
    """
    A class for the combination of classifications
    """

    def __init__(self, classifications: Iterable) -> None:
        """
        Constructor
        """

        # Get metadata
        self.nclassifications=len(classifications)

        # Make sure that there is at least one classification available
        assert (self.nclassifications>0), "no classifications available"

        # Combine the available categories

        # Get metadata
        self.categories=classifications[0].categories
        for iclassification in range(1, self.nclassifications):
            for category in classifications[iclassification].categories:
                if(category not in self.categories):
                    self.categories.append(category)
        
        # Get metadata
        self.ncategories=len(self.categories)
        
        # Make sure that there is at least one category available
        assert (self.ncategories>0), "no categories available"

        # Combine the available items

        # Determine the items of the combined classification
        self.items=classifications[0].items
        for iclassification in range(1, self.nclassifications):
            for item in classifications[iclassification].items:
                if(item not in self.items):
                    self.items.append(item)
        
        # Get metadata
        self.nitems=len(self.items)

        # Make sure that there is at least one item available
        assert (self.nitems>0), "no items available"

        # Combine the classifications

        # Initialize the comments on each item
        self.comments=[[] for iitem in range(self.nitems)]

        # Initialize the times an items falls in each category
        self.ntimesInCategory=np.zeros((self.nitems, self.ncategories), dtype=int)

        # Determine the comments and number of times each item falls in each category
        for classification in classifications:
            for iitem in range(classification.nitems):
                ilocalItem=self._classification__getItemID(classification.items[iitem])
                itemCategories=classification.itemCategories[iitem]
                for itemCategory in itemCategories:
                    ilocalCategory=self._classification__getCategoryID(itemCategory)
                    self.ntimesInCategory[ilocalItem, ilocalCategory]=self.ntimesInCategory[ilocalItem, ilocalCategory]+1
                itemComments=classification.itemComments[iitem]
                self.comments[ilocalItem].append(itemComments)

        # Return
        return
    
    def getCategoriesOf(self, item: str, threshold: int = 1) -> list:
        """
        Return the categories of the specified item

        Parameters
        ----------
        item : str
            The item the categories of which to return
        threshold : int
            The number of times the item must have fallen within a category in order for that category to be returned
        """

        # Determine the categories to be returned
        shouldReturnCategory=(self.ntimesInCategory[self._classification__getItemID(item),:]>=threshold)
        categoriesToReturn=[]
        for icategory in range(self.ncategories):
            if(shouldReturnCategory[icategory]):
                categoriesToReturn.append(self.categories[icategory])

        # Return
        return categoriesToReturn
    
    def getCommentsOn(self, item: str) -> list:
        """
        Return the comments on the specified item

        Parameters
        ----------
        item : str
            The item the comments on which to return
        """

        # Return
        return self.comments[self.__getItemID(item)]
    
    def getNumberOf(self, category: str, threshold: int = 1) -> int:
        """
        Determine the number of items in the specified category

        Parameters
        ----------
        category : str
            The category the number of items in which to determine
        threshold : int
            The number of times an item must have fallen within the category in order to be taken into account
        """

        # Return
        return int(np.sum(self.ntimesInCategory[:,self._classification__getCategoryID(category)]>=threshold))

    def getFractionOf(self, category: str, threshold: int = 1) -> float:
        """
        Determines the fraction of items in the specified category

        Parameters
        ----------
        category : str
            The category the fraction of items in which to determine
        threshold : int
            The number of times an item must have fallen within the category in order to be taken into account
        """

        # Return
        return float(self.getNumberOf(category, threshold=threshold)/self.nitems)

    def getItemsIn(self, category: str, threshold: int = 1) -> list:
        """
        Return the items in the specified category

        Parameters
        ----------
        category : str
            The category the items in which to return
        threshold : int
            The number of times an item must have fallen within the category in order to be taken into account
        """

        # Determine the items to be returned
        shouldReturnItem=(self.ntimesInCategory[:,self._classification__getCategoryID(category)]>=threshold)
        itemsToReturn=[]
        for iitem in range(self.nitems):
            if(shouldReturnItem[iitem]):
                itemsToReturn.append(self.items[iitem])

        # Return
        return itemsToReturn

#############
# Functions #
#############

#****************#
# Get categories #
#****************#

def getCategories(category: dict, depth: int = 0) -> dict:
    """
    Returns the all the individual classification categories of a categories dictionary

    Parameters
    ----------
    category : dict
        The dictionary of the category the subcategories of which are to be returned
    depth : int, optional
        The recursion depth of the current call (default is 0)
    """

    # Initialize the subcategories dict
    if(depth>0):
        categories=[category['name']]
    else:
        categories=[]

    # Add the subcategories of the category to the dictionary
    for subcategory in category['categories']:
        categories.extend(getCategories(subcategory, depth=depth+1))
    
    # Return
    return categories

#**********************#
# Read categories file #
#**********************#

def readCategoriesFile(file: str) -> list:
    """
    Reads and parses the categories of a categories JSON file

    Parameteres
    -----------
    file : str
        The path to the categories file
    """

    # Read the categories file
    categories=readJSONFile(file)

    # Return
    return getCategories(categories)

#**********************#
# Read classifications #
#**********************#

def readClassifications(files: list, categories: list, combine: bool = False) -> Union[list, combinedClassification]:
    """
    Reads and parses a list of classification files

    Parameteres
    -----------
    files : list
        The paths to the classification files
    categories : list
        The categories of the classification
    combine : bool, optional
        Should we combine the classification data? (default is False)
    """

    # Get metadata
    nclassifications=len(files)

    # Initialize the classifications list
    classifications=[]

    for iclassification in range(nclassifications):

        # Read the classification file
        fileClassification=readJSONFile(files[iclassification])

        # Get metadata
        nfileGalaxies=len(fileClassification['galaxies'])

        # Allocate the required memory
        fileNames=[]
        fileCategories=[]
        fileComments=[]

        # Parse the data of the classification
        for igalaxy in range(nfileGalaxies):
            fileNames.append(fileClassification['galaxies'][igalaxy]['name'])
            fileCategories.append(fileClassification['galaxies'][igalaxy]['categories'])
            fileComments.append(fileClassification['galaxies'][igalaxy]['comments'])

        # Initialize the classification
        classifications.append(classification(fileNames, fileCategories, fileComments, categories))

    # Return
    return classifications