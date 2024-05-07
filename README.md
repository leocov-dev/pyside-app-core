# pyside-app-core

Custom style, widgets, and utilities for cross-platform PySide6 applications with a focus on 'frameless' styling.

> This project should be considered experimental and subject to breaking changes until a 1.0.0 release.


### Install

```shell
$ pip install pyside-app-core
```


## Local Development

```shell
$ poetry install
```


### Run example application

```shell
$ poetry run python -m examples.toolbar_app --generate-rcc
```

### Generate resources files

Resource files MUST be generated at least once for stylesheets and icons to function.

```shell
# from repo with this lib installed
poetry run compile-pyside-theme a/target/directory

# custom QssTheme subclass where `./theme.py` has `THEME = CustomTheme()`
poetry run compile-pyside-theme \
    --custom-theme-pypath theme.THEME \
    a/target/directory

# if needed to resolve python modules you can include pypath updates
poetry run compile-pyside-theme \
    --extra-python-path ./src \
    --custom-theme-pypath src.example_app.theme.THEME \
    a/target/directory
```