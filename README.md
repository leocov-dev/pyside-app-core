# pyside-app-core

Custom style, widgets, and utilities for cross-platform PySide6 applications.

> 🚧 🚧 🚧 NOTICE 🚧 🚧 🚧
>
> This project should be considered experimental and subject to breaking changes until a 1.0.0 release.


![GitHub Release](https://img.shields.io/github/v/release/leocov-dev/pyside-app-core)
![GitHub License](https://img.shields.io/github/license/leocov-dev/pyside-app-core)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/leocov-dev/pyside-app-core/ci.yml)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/pyside-app-core)


### Install

To use `pyside-app-core` as a library in your own projects install the [wheel distribution](https://pypi.org/project/pyside-app-core/) from PyPi

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

You must run the examples from the repository root directory.

```shell
hatch run examples:toolbar_app
```

### Run tests

Hatch can run tests across multiple versions of python.

```shell
hatch test -a -p
```

### Generate resources files

Resource files MUST be generated at least once in the project using this library for icons to function.

When installed this library provides a cli tool `pyside-app-core-compile-rcc` that aids in generating a `resources.rcc` file.

```shell
# from repo with this lib installed
pyside-app-core-compile-rcc a/target/directory
```