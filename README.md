# PyCalc
[![Build Status](https://travis-ci.org/Deedasmi/PyCalc.svg)](https://travis-ci.org/Deedasmi/PyCalc)
A command line calculator written in Python.

## Installation

PyCalc is not currently hosted on PyPi. For now, download the source and use pip or distutils to install.
Example:
```
git clone https://github.com/Deedasmi/PyCalc.git
python setup.py install
# or pip install .
```

## Usage

PyCalc may be used by importing (from pycalc import calc), or as a standalone program by using python -m pycalc

PyCalc supports standard operators (+-/*^%), as well as some alternate character []{}\

Additionally, you may define your own variables (foo = 21) and functions (foobar(foo, bar) = foo * bar)
To access the variables, simply use the variable name in the function (foo * 2).
Functions may currently only be used as a single statement(foobar(21, 2)).