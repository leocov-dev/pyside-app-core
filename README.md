# pyside-app-core

Custom style, widgets, and utilities for cross-platform PySide6 applications.

> [!WARNING]
>
> This project should be considered experimental and subject to breaking changes 
> AT ANY TIME until a v1.0.0 release.


![GitHub Release](https://img.shields.io/github/v/release/leocov-dev/pyside-app-core)
![GitHub License](https://img.shields.io/github/license/leocov-dev/pyside-app-core)
[![CI](https://github.com/leocov-dev/pyside-app-core/actions/workflows/ci.yml/badge.svg)](https://github.com/leocov-dev/pyside-app-core/actions/workflows/ci.yml)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/pyside-app-core)


### Install

To use `pyside-app-core` as a library in your own projects install the 
[wheel distribution](https://pypi.org/project/pyside-app-core/) from PyPi

```shell
$ pip install pyside-app-core
```


## Local Development

Requirements:
- Hatch ([installation instructions](https://hatch.pypa.io/latest/install/))

```shell
hatch env create
```

### Run example application

An example project/application is included

```shell
# switch to the example project dir
cd examples/toolbar-app-project
# build the project
hatch build -t pyside-app --clean
# list the build artifacts
ls dist
```

### Run tests

Hatch can run tests across multiple versions of python.

```shell
hatch test -a -p
```

### Hatch Build Plugin

This library exposes a `hatch` build plugin that will generate Qt resources and
package a standalone executable. See the example project for details.
