###########
# Imports #
###########

# System #

import json

# Local #

from ..misc import Console

#############
# Functions #
#############

#****************#
# Read JSON file #
#****************#

def readJSONFile(inputFile: str, quiet: bool = False) -> dict:
    """
    Reads the data of an input JSON file as a dictionary

    Parameters
    ----------
    inputFile : str
        The path to the input file
    quiet : str, optional
        Should the console output be suppressed? (default is False)
    """

    if(not quiet):
        Console.pushJob("Reading JSON file...")
    
    # Open file for reading
    file=open(inputFile, mode='r')

    # Read the JSON data of the file
    data=json.load(file)

    # Close the file
    file.close()

    if(not quiet):
        Console.popJob(success=True)
    
    # Return
    return data

#*****************#
# Write JSON file #
#*****************#

def writeJSONFile(outputFile: str, data: dict, indent: int = 4, quiet: bool = False) -> None:
    """
    Writes the data of a dictionary as a JSON file

    Parameters
    ----------
    outputFile : str
        The path to the output file
    quiet : str, optional
        Should the console output be suppressed? (default is False)
    """

    if(not quiet):
        Console.pushJob("Writing output file...")
    
    # Open file for writing
    file=open(outputFile, mode='w')

    # Write the JSON data to the file
    json.dump(data, file, indent=indent)

    # Close the file
    file.close()

    if(not quiet):
        Console.popJob(success=True)
    
    # Return
    return