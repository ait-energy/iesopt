# Improving the documentation

## Building locally

```bash
sphinx-build --nitpicky --fail-on-warning --fresh-env --keep-going --builder html docs/ docs/_build/html
```

You can omit the `--fresh-env` option to not

```text
--fresh-env, -E       don't use a saved environment, always read all files
```

and alternatively use

```bash
make -C docs clean
```

to clean the `docs` before rebuilding them.

:::{admonition} Note on `--keep-going`
:class: caution
A final build of updates to the documentation, that is built using the `--fail-on-warning` flag, should be done without
`--keep-going`, to prevent skipping warnings/errors: Each warning (or subsequent error) should be properly resolved!
:::
