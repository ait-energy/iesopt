# Contributing

Thank you for your interest in contributing to `iesopt`! This guide provides instructions on setting up your development environment and contributing code.

## Setting up the development environment

1. **Fork the Repository:** First, fork the main repository on GitHub to your account.
2. **Clone the Repository:** Clone the forked repository to your local machine, by running

    ```bash
    git clone https://github.com/your-username/iesopt.git
    cd iesopt
    ```
3. **Install uv:**
    Please follow the official [uv install instructions](https://docs.astral.sh/uv/getting-started/installation/)


4. **Create the virtual environment:** To setup the development venv run

    ```bash
    uv sync
    ```
The virtual environment is now located in the ```.venv``` folder (if you ever need to start over, you can just delete this folder)

5. **Pre-commit Hooks:** To maintain code quality, please install the pre-commit hooks:

    ```bash
    uv run pre-commit install
    ```

## Code formatting and linting

After installing pre-commit hooks before, all checks should be automatically run and applied when committing changes.

:::{admonition} Manually running checks
:class: dropdown

You can either execute

```bash
uv run pre-commit
```

This stashes all changes that you have not committed. If you want to check all files, as they are, you can do so by running:

```bash
uv run pre-commit run --all
```

:::

`ruff` (our linter & formatter) should fix most mistakes automatically. `codespell` (our spelling checker) however, will report on mistakes in the terminal, linking to their occurrence. Inspect them, and fix them accordingly. Consult their [README](https://github.com/codespell-project/codespell) if you (highly unlikely) encounter a word where it wrongfully triggers.

## Running tests

To run the test suite in your dev environment do

```bash
uv run pytest
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

### Running tox tests
To run the test suite against all compatible Python versions do

```bash
uv run tox
```

## Making changes

1. **Create a New Branch**: Always create a new branch for your work:

    ```bash
    git checkout -b new-fix-or-feature
    ```

2. **Make Your Changes**: Edit files and make your desired changes.

3. **Test Your Changes**: Run tests frequently to ensure nothing is broken.

4. **Commit Your Changes**: Follow conventional commit messages for clarity:

    ```bash
    git commit -m "feat: added new feature X"
    ```

5. **Push Your Changes**: Push the changes to your fork:

    ```bash
    git push origin new-fix-or-feature
    ```

## Improving the documentation

### Building locally

```bash
uv run sphinx-build --nitpicky --fail-on-warning --fresh-env --keep-going --builder html docs/ docs/_build/html
```

You can omit the `--fresh-env` option to not

```text
--fresh-env, -E       don't use a saved environment, always read all files
```

and alternatively use

```bash
uv run make -C docs clean
```

to clean the `docs` before rebuilding them.

:::{admonition} Note on `--keep-going`
:class: caution
A final build of updates to the documentation, that is built using the `--fail-on-warning` flag, should be done without
`--keep-going`, to prevent skipping warnings/errors: Each warning (or subsequent error) should be properly resolved!
:::

## Submitting a pull request (PR)

Once your changes are pushed to your fork, you can submit a pull request to the main repository:

1. **Open a Pull Request**: Go to the [main repository](https://github.com/ait-energy/iesopt) and click "New Pull Request."
2. **Follow the Template**: Provide a clear title and description of your changes.
3. **Respond to Feedback**: Engage with reviewers and make requested changes promptly.

## Code Style and Guidelines

- **Follow PEP 8**: Ensure your code adheres to [PEP 8](https://www.python.org/dev/peps/pep-0008/).
- **Document Your Code**: Provide docstrings for all functions, classes, and modules.
- **Write Tests**: Include tests for new features and bug fixes.

## Reporting issues

If you find any bugs or have feature requests, please report them via the [issue tracker](https://github.com/ait-energy/iesopt/issues).
