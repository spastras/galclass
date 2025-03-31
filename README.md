# GalClass

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
python3 -m pip install .
```

## Usage

In order to use `galclass` you can launch it from the command line, using the `-c` command line argument and specifying the path to the categories file to be used:

```console
python3 -m galclass -c path/to/categories.json
```

If you would just like to browse through the input files skipping the classification part, you can omit the `-c` command line argument as well as specifying the path to a categories file.

Once the main window shows up on your screen, you can just drap and drop an input file list into it to get started.

If you prefer to specify the path to the input file list in the terminal, you can call `galclass` using the `-i` command line argument:

```console
python3 -m galclass -c path/to/categories.json -i path/to/inputFileList.json
```

## Navigation

If you would like to use the keyboard in order to browse through the input files, you can do so using:

* `Right Arrow` / `Left Arrow` to view the `Next` / `Previous` filter of a galaxy
* `Shift`+`Right Arrow` / `Shift`+`Left Arrow` to view the `Next` / `Previous` galaxy

## Acknowledging

If you use GalClass, we ask that you cite the following paper:

* Espejo Salcedo et al., 2025 (submitted) [https://ui.adsabs.harvard.edu/abs/2025arXiv250321738E](https://ui.adsabs.harvard.edu/abs/2025arXiv250321738E)

## Support & Development

If you have any questions, suggestions or bug reports please don't hesitate to contact me!