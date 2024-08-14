# Contributing

## How to contribute

Check our Github repository.

## Developing IESopt

### `iesopt`

#### Setup

To be added.

#### Code formatting and linting

1. Install `pre-commit` by running `pre-commit install`
2. Now all checks should be automatically run and applied when committing changes

You can manually run those by executing

```bash
pre-commit
```

This stashes all changes that you have not committed. If you want to check all files, as they are, you can do so by running:

```bash
pre-commit run --all
```

`ruff` (our linter & formatter) should fix most mistakes automatically. `codespell` (our spelling checker) however, will report on mistakes in the terminal, linking to their occurrence. Inspect them, and fix them accordingly. Consult their [README](https://github.com/codespell-project/codespell) if you (highly unlikely) encounter a word where it wrongfully triggers.

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
