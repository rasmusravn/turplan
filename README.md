# turplan

[![PyPI](https://img.shields.io/pypi/v/turplan.svg)](https://pypi.org/project/turplan/)
[![Changelog](https://img.shields.io/github/v/release/rasmusravn/turplan?include_prereleases&label=changelog)](https://github.com/rasmusravn/turplan/releases)
[![Tests](https://github.com/rasmusravn/turplan/actions/workflows/test.yml/badge.svg)](https://github.com/rasmusravn/turplan/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/rasmusravn/turplan/blob/master/LICENSE)

CLI program til at holde styr på en kommende tur

## Installation

Install this tool using `pip`:
```bash
pip install turplan
```
## Usage

For help, run:
```bash
turplan --help
```
You can also use:
```bash
python -m turplan --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd turplan
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
