# galclass

[![PyQt6 >=6.4.0](https://img.shields.io/badge/PyQt6->=6.4.0-red.svg)](https://pypi.org/project/PyQt6/6.4.0/)
[![numpy >=1.13.0](https://img.shields.io/badge/numpy->=1.13.0-green.svg)](https://pypi.org/project/numpy/1.13.0/)
[![Python >=3.6.1](https://img.shields.io/badge/Python->=3.6.1-blue.svg)](https://www.python.org/downloads/release/python-361/)

## Description

A module for the morphological classification of galaxies using `Qt`.

This module is intended to be used as a generic classification tool, as the categories of the classification can be dynamically specified during execution.

This tool has been heavily based on a classification script by `G. Mahler`, modified by `Daizhong Liu` and `Juan Espejo`.

## Installation

You can install this module using `pip`:

```console
$ python3 -m pip install .
```

## Usage

In order to use `galclass` you should launch it from the command line, specifying the path to the categories file to be used:

```console
$ python3 -m galclass -c path/to/categories.json
```

Once the main window shows up on your screen, you can just drap and drop an input file list into it to get started.

If you prefer to specify the path to the input file list in the terminal, you can call `galclass` using the `-i` command line argument:

```console
$ python3 -m galclass -c path/to/categories.json -i path/to/inputFileList.json
```

## Development

If you have any suggestions or bug reports please don't hesitate to contact me!