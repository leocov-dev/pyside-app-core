# pyside-app-core

Custom style, widgets, and utilities for PySide 6.5 applications.

> This project should be considered experimental and subject to breaking changes at any time.


### Install

```shell
$ pip install pyside-app-core
```


### Run example application

```shell
$ python -m examples.simple_app --generate-rcc
```

### Generate resources files

Resource files MUST be generated at least once for stylesheets and icons to function.

```shell
# from repo with this lib installed
$ compile-pyside-theme <target directory>

# custom QssTheme subclass where `./theme.py` has `THEME = CustomTheme()`
$ compile-pyside-theme <target directory> --custom-theme-pypath theme.THEME

# if needed to resolve python modules you can include pypath updates
$ compile-pyside-theme <target directory> --extra-python-path ./src --custom-theme-pypath src.example_app.theme.THEME
```