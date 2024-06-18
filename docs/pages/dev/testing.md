# Tests & Code Quality

## Format and lint

Use

```bash
black src/ docs/conf.py
black docs/notebooks
ruff check .
```

Commit pure formatting changes using `chore: formatting`.

## Running tests

```bash
pytest
```

This will print a coverage report, which looks like

```text
Name                           Stmts   Miss  Cover
--------------------------------------------------
src/iesopt/__init__.py            33      4    88%
src/iesopt/general.py              0      0   100%
...
src/iesopt/util/logging.py         7      0   100%
src/iesopt/util/util.py            5      0   100%
--------------------------------------------------
TOTAL                            417    172    59%
```

and tells you roughly how good each file is covered by automated tests. Further it creates a `coverage.xml` file in the project root folder, that you can use. In `VSCode`, the extension [Coverage Gutters](https://marketplace.visualstudio.com/items?itemName=ryanluker.vscode-coverage-gutters) allows inspecting test coverage directly in your code editor. If you have it installed and loaded, simply hit `Ctrl + Shift + 8` (if you are using default keybinds) to enable watching the coverage.

