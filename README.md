# pyside-app-core

Custom style, widgets, and utilities for cross-platform PySide6 applications with a focus on 'frameless' styling.

> This project should be considered experimental and subject to breaking changes until a 1.0.0 release.


### Install

```shell
$ pip install pyside-app-core
```


## Local Development

```shell
$ poetry env use 3.11
$ poetry install --no-root --with dev
$ poetry run pre-commit install
```


### Run example application

```shell
$ poetry run python -m examples.toolbar_app --generate-rcc
```

### Generate resources files

Resource files MUST be generated at least once in the project using this library for icons to function.

```shell
# from repo with this lib installed
poetry run pyside-app-core-compile-rcc a/target/directory
```