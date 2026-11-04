# Updating

This page collects information about updating the project between specific versions.

## Pre-2.13 to 2.13.0

Version 2.13.0 introduced an updated IESopt.jl version, which requires a note on how to upgrade existing environments.
The most important change is a mandatory move to Julia `1.12` and Python `3.14`; the latter could be relaxed in the
future if needed, but using `>= 3.14` simplifies matching OpenSSL versions between Julia and Python by a lot (many
"versions" of CPython make use of an outdated OpenSSL with some "crucial insecurities", which breaks using Julia/Python
together).

Follow these steps, but please report any issues you encounter immediately to the dev chat, so that we can fix/document
problems that might arise with slightly differing initial setups:

First, make sure your `uv` is up-to-date, by running:

```bash
uv self update
```

Update the required Python version in your `pyproject.toml` by setting it to:

```toml
requires-python = ">=3.14"
```

Set a specific Python version in your `.python-version` file (note: this version prevents pulling an outdated CPython
build as of 17.02.2026; might require a different version in the future), by changing its content to:

```text
3.14.3
```

Update the `iesopt` version in your `pyproject.toml` to (at least) `2.13.0` by running

```bash
uv add "iesopt >= 2.13.0"
```

:::{caution}
If this step fails with an error that mentions `pandas>=3.0.0` being required by your project, run
`uv add "pandas < 3.0"` first, then rerun the above command.
:::

You should now be able to run:

```bash
uv run python
>>> import iesopt
```

If this succeeds (after some time to precompile the new version), then you are good to run any model as you are used to.

### Read on: JuliaUp

If you encounter a log message like this:

```console
WARNING: About to install Julia ... to ...
         If you use juliapkg in more than one environment, you are likely to
         have Julia installed in multiple locations. It is recommended to
         install JuliaUp (https://github.com/JuliaLang/juliaup) or Julia
         (https://julialang.org/downloads) yourself.
```

we highly recommend following that advice and installing `juliaup`. This is nowadays done automatically when you install
Julia from the official homepage [julialang.org/](https://julialang.org/downloads/):

> juliaup is the recommended way to install Julia. It automatically installs the latest stable julia binary and helps
> keep it up to date. It also supports installing and using different versions of Julia simultaneously.

This most importantly means that if you have `juliaup` installed, IESopt can reuse this across different projects that
you work on, heavily reducing the setup time since there's no need to download a full Julia for each project and a lot
of precompilation stuff can be shared.

## 2.6.3 to 2.6.4 or 2.6.5

When upgrading from a version between `2.0.0` and `2.6.3` to either `2.6.4` or `2.6.5` you may run into an error looking similar to

```python
Exception: 'version' entries have empty intersection:
- '=1.25.0' at <YOUR_PROJECT>/.iesopt/juliapkg.json
- '=1.24.0' at <YOUR_PROJECT>/.venv/lib/site-packages/iesopt/juliapkg.json
```

where `<YOUR_PROJECT>` is the path to your project that uses iesopt.
You can fix this manually by deleting the old file at `<YOUR_PROJECT>/.venv/lib/site-packages/iesopt/juliapkg.json`.
If you upgrade to `2.6.6` or higher you will not run into this issue.

## 1.x.y to 2.0.0

The `2.0.0` release follows the breaking change of `IESopt.jl` going to `v2.0.0`. This was mainly triggered by a proper rework of how addons work, including a new internal handling for more complex expressions (allowing more flexibility in configuring `conversion`, or `cost` settings), as well as better support around templates (e.g. the introduction of `Virtual`s). A few breaking changes that were planned for quite some time are part of this.

### Changes to the top-level config

The structure of the `config` section in the top-level configuration file changed. Overall it's highly similar, but:

- A `general` section was added that properly groups "general" settings, that were previous keyword arguments.
- Small adjustments were made to account for that.
- The `results` section changed slightly.

See the respective section(s) in the [YAML/Top-level config](../manual/yaml/top_level.md) documentation. The most important changes relate to the following (sub-)sections:

- `name`
- `version`
- `high_performance`
- `constraint_safety` is now called `soft_constraints` and part of the `optimization` section.

### Changes to keyword arguments

Previously we allowed passing arbitrary keyword arguments to public functions, like {py:func}`iesopt.Model.generate` or {py:func}`iesopt.run`. This can lead to problems with latency on previously unseen types of arguments, especially now that we support arbitrary dictionaries as model parameters. This now works differently:

- There are no arbitrary keyword arguments anymore.
- Model parameters have to be passed as dictionary, using `parameters = {foo: 1.0, bar: "austria"}`.
- There is a new and "powerful" `config` keyword argument, explained below.

#### `config`

Besides model parameters, specific keyword arguments existed, e.g., `verbosity`. These are gone and now first-class options in the model's top-level config (see [YAML/Top-level config](../manual/yaml/top_level.md)). With that a way to change them programmatically was in need, which is what the `config` argument does. Take the following example:

```{code-block} python
:caption: Example usage of `config` keyword argument.

import iesopt

iesopt.run("my_config.iesopt.yaml", config = {
    "general.verbosity.core": "error",
    "optimization.snapshots.count": 168,
    "files.data_in": "scenario17/data.csv",
})
```

The passed dictionary modifies the top-level configuration during the parsing step. That means you are able to overwrite / set each configuration option programmatically. The access pattern follows the structure of the `config` section in the top-level configuration file. For example, the verbosity in the YAML looks like:

```{code-block} yaml
:caption: Verbosity example in the top-level YAML.

config:
  general:
    verbosity:
      core: info
```

To modify / set this, `general.verbosity.core` is used. As you can see that opens the possibility to modify, e.g., files that are loaded based on (for example) which scenario we are in by modifying the `files` section, using `files.data_in`. Here `data_in` is the "name" used in the model later on (using `some_col@data_in`).

Further, this means you no longer need to use "model parameters" for stuff that is actually part of the `config` section, e.g., the number of Snapshots in your model. Instead of coming up with a parameter, e.g., `my_snapshot_count`, using it as `count: <my_snapshot_count>`, and then passing it as `iesopt.run("...", my_snapshot_count = 168)`, you can now just modify that as shown above by setting it using the accessor `optimization.snapshots.count`.

#### `parameters`

Any dictionary passed to this will be used in the same way as keyword arguments were used before: Parameters given there are replaced in the `parameters` section (which might be based on an external `*.iesopt.param.yaml` file).

### Changes to result extraction

We saw increasing interest in actively "filtering" results of various models. This triggered the implementation of a new result backend (initially only JLD2) supported by DuckDB. This is (as of 2.0.0) not enabled as default, since it does not fully support the functionality that the Python wrapper `iesopt` provides. However, we plan on switching to this backend in the future.

### Changes to addons

To be written: Link to addon page/docs as soon as they are done.

### Changes to examples, and more

Everything that was previously part of `IESoptLib.jl` is now integrated into `IESopt.jl`. Functionality around this can be accessed using `IESopt.Assets`.

### Other changes

#### Tags

Component "tags" are back (or accessible again, they were never gone completely). That means you can tag components to later simplify result handling or working with your model. A tag can be added when creating a component:

```{code-block} yaml
:caption: Adding a tag.

components:
  my_unit:
    type: Unit
    tags: CustomUnit
```

The attribute `tags` supports single tags (e.g., `CustomUnit`) or lists of tags (e.g., `[CustomUnit]` or `[CustomUnit, FindMe]`).

:::{tip}
Each core component automatically tags its own type, so each `Unit` will already be tagged with the tag `"Unit"`.

Most importantly, that means you are also able to extract all `Virtual`s (non-existing components related to templates that you use), since each of these also tags its "actual type".
:::

Using this is possible with {py:func}`iesopt.Model.get_components`:

```{code-block} python
:caption: Extracting tagged components.

import iesopt

model = iesopt.run("tagged_model.iesopt.config")

my_units = model.get_components("CustomUnit")
```

When passing a `list` of tags, only components having ALL of these tags are returned.

:::{tip}
Most importantly, that (and the fact that components "auto-tag" their type) means you are also able to extract all `Virtual`s (non-existing components related to templates that you use), since each of these also tags its "actual type". Consider a template `Battery` that you use to initialize a battery

```yaml
components:
  my_bat:
    type: Battery
```

All batteries can then be found using `model.get_components("Battery")`. This can also be really helpful in addons, where (using Julia) you can find, e.g., all CHPs in your model by doing `chps = IESopt.get_components(model; tagged="CHP")`.
:::
