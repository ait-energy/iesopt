# Top-level config

The top-level YAML configuration file, often named `config.iesopt.yaml`, is the main configuration file for the IESopt optimization model. It may contain the following main sections:

1. `parameters` (optional): General global parameters.
2. `config`: General configuration settings for the optimization model.
3. `addons` (optional): Additional settings for specific addons.
4. `carriers`: Definition of all energy carriers.
5. `components` (and/or `load_components`): Definitions of core components.

```{note} As mentioned in the [intro section](./index.md) of the YAML reference, dictionaries are considered to not guarantee order. Therefore, the order of the sections in the YAML file is not important - however, the order given above is recommended for readability.
```

This means a basic top-level configuration file could look like this:

```{code-block} yaml
:caption: Rough outline of a simple `config.iesopt.yaml`.

config:
  optimization:
    problem_type: LP
    snapshots:
      count: 24

carriers:
  electricity: {}

components:
  main_grid_node:
    type: Node
    carrier: electricity
```

## `parameters`

General global parameters, that the whole model can access. Can be set from outside when, e.g., when calling {py:func}`iesopt.run`.

```{note}
This section is optional and only needed if you want to global model parameters.
```

The base approach is passing a dictionary, with all global parameters and their default values:

```{code-block} yaml
:caption: Example for a `dict`-based `parameters` section.

parameters:
  ng_emission_factor: 0.202
  co2_cost: 125
  elec_cost: null
```

Here `elec_cost` defaults to `null` - which is the equivalent of `None` (Python) or `nothing` (Julia). Either it is used internally for some setting that accepts `null` as a valid value, or it is meant to be set from outside.

However, with a growing number of parameters, it might be more convenient to store them in a separate file. This can be done by passing the path to the file:

```{code-block} yaml
:caption: Example for file-based `parameters` section.

parameters: global_params_scenarioHIGH.iesopt.param.yaml
```

The file `global_params_scenarioHIGH.iesopt.param.yaml` could then look like this:

```{code-block} yaml
:caption: Example content of `global_params_scenarioHIGH.iesopt.param.yaml`.

ng_emission_factor: 0.202  # t CO2 / MWh_ng
co2_cost: 125              # EUR / t CO2
elec_cost: null            # EUR / MWh_el
```

```{hint}
Make sure to use comments to better explain the parameters and their units, and structure the file in a way that makes it easy to read and understand. Note: The same is true for the dictionary approach - use comments! - but the file approach is more likely to be used with a large number of parameters.
```

## `config`

General configuration settings for the optimization model.

```{code-block} yaml
:caption: Example for the `config` section in the top-level YAML configuration file.

config:
  general:
    version:
      core: 1.1.0
      python: 1.4.7
    name:
      model: FarayOptIndustry
      scenario: Base_2022_LOW
  optimization:
    problem_type: LP
    snapshots:
      count: 168
  files:
    data: inputs_2022.csv
  results:
    enabled: true
  paths:
    files: data/
    templates: templates/
    components: model/
    results: out/
```

The following subsections explain each part of the `config` section in more detail.

### `general`

This contains general settings.

#### `version`

This section allows specifying various IESopt versions, which is important to ensure reproducibility and compatibility: Executing a model based on a `config.iesopt.yaml` file with a different version of IESopt might lead to **unexpected results or errors**.

```{code-block} yaml
:caption: Example for the `version` section.

config:
  general:
    version:
      core: 1.1.0
      python: 1.4.7
```

We try to stick to [semantic versioning](https://semver.org/), which means that changes to the minor or patch version should not contain breaking changes, but:

1. A bug fix to `IESopt.jl` might lead to different results of your model, meaning every bug fix might be a breaking change "for you".
2. We might mess up and introduce a breaking change in a minor version, without intending it.

Therefore: Make sure you **KNOW** what changes between versions, and **TEST** your models when upgrading.

:Parameters:
:`core`: The version of the core IESopt framework (`IESopt.jl`).
:`python`: The version of the Python interface (`iesopt`).

:::{tip}
You may add arbitrary versions to this section, e.g., for personal use in specific addons or other dependencies.
:::

#### `name`

This section does not directly affect the model but can be used to store the name of the model and the scenario. This can be useful for logging and debugging purposes, as well as for the results output.

```{note}
This section is optional and only needed if you want to global model parameters.
```

:Parameters:
:`model`: Name of the model, e.g., a high-level description, or the name of the project.
:`scenario`: A specific scenario or case, e.g., the year, a specific set of parameters, or a version of input files.

```{tip}
The `scenario` setting supports dynamic placeholders. Currently, you can use `$TIME$` which will automatically be replaced by the timestamp of the model being built. This way, each result will have a unique scenario name, which prevents overwriting results.
```

Consider the following example for the `name` section:

```{code-block} yaml
:caption: Example for the `name` section.

config:
  general:
    name:
      model: FarayOptIndustry
      scenario: Base_2022_LOW_T-$TIME$
```

When running the model containing this configuration, the results will be stored in a folder structure that looks like this:

```{code-block} text
:caption: Example folder structure for the results of the model run.

.
├── data/
│   └── ...
├── out/
│   ├── FarayOptIndustry/
│   │   ├── Base_2022_LOW_T-2024_09_11_09520837.iesopt.result.jld2
│   │   ├── Base_2022_LOW_T-2024_09_11_09520837.iesopt.log
│   │   ├── Base_2022_LOW_T-2024_09_11_09520837.highs.log
│   │   └── ...
│   └── FarayOptIndustry_Baseline/
│       └── ...
└── config.iesopt.yaml
```

In this example, the `$TIME$` placeholder was replaced by the current timestamp, which is `2024_09_11_09520837` in this case. You can see the top-level config file (`config.iesopt.yaml`), a data folder (`data/`; see the [files](#files) and [paths](#paths) sections), the results folder (`out/`; see the [results](#results) and [paths](#paths) sections). Inside the results folder, IESopt creates a folder for each "model name". Each executed run creates its result files inside that, using the "scenario name" as base filename.

#### `verbosity`

Controls the verbosity of various parts of a model run.

:Parameters:
:`core` (`str`, default = `info`): Verbosity of the (Julia) core, `IESopt.jl`. Supports: `debug`, `info` (default), `warning`, `error`.
:`progress` (`str`): Whether to show progress bars (`on` or `off`), defaults to `on` unless `core` is set to `error` - in that case it defaults to `off`.
:`python` (`str`): Verbosity of the Python wrapper, `iesopt`. Supports: `debug`, `info`, `warning`, `error`. Defaults to the verbosity set in `core`.
:`solver` (`str`): Whether to silence solver prints/outputs (`on` or `off`), defaults to `on` unless `core` is set to `error` - in that case it defaults to `off`.

#### `performance`

Controls various "performance" related settings of the model.

:Parameters:
:`string_names` (`bool`, default = `true`): Activates (or deactivates) "string names" for expressions, variables, and constraints. These make the model readable for humans, but cost (a lot of) performance. Refer to the [`JuMP.jl` documentation](https://jump.dev/JuMP.jl/stable/tutorials/getting_started/performance_tips/#Disable-string-names) and its `set_string_names_on_creation` function, or read upon how this upstream functionality originated from a discussion during the early stages of IESopt development ([discourse.julialang](https://discourse.julialang.org/t/optimal-model-creation-and-garbage-collection/72619), [this issue](https://github.com/jump-dev/JuMP.jl/issues/2817), and some time later [this PR](https://github.com/jump-dev/JuMP.jl/pull/2978)).
:`logfile` (`bool`, default = `true`): Controls whether or not to write an IESopt logfile (which captures everything even if verbosity prevents displaying it). While this does save a bit of time it also prevents tracking down errors, so disable it wisely. This is most important to disable in iterative solves of small models, where logging accounts for a larger portion of overall time.
:`force_addon_reload` (`bool`, default = `true`): If set to `false`, addons that have already been loaded once will not be reloaded. This can help with repeated solves of the same model. Be aware, that this might interfere with reloading changes to an addon's code that you have made, so unless you need it (and understand it) it is best left as `true`.

```{code-block} yaml
:caption: Example for the `performance` section.

config:
  general:
    performance:
      string_names: false
      logfile: true
```

### `optimization`

#### `problem_type`

:Options:
:`LP`: Restricted to (continuous) linear programming formulations.
:`MILP`: Enables mixed-integer linear programming formulations.
:`MO`: Enables multi-objective optimization formulations.
:`MGA`: Enables modelling-to-generate-alternatives formulations.
:`SDDP`: Enables stochastic dual dynamic programming formulations.

Options can be combined using `+` (where applicable), e.g., `LP+MO`.

```{code-block} yaml
:caption: Example for the `problem_type` section.

config:
  optimization:
    problem_type: LP
```

```{note}
The options `MO`, `MGA`, and `SDDP` represent very advanced functionality. These are not fully documented, or may be partially broken in any given release. If you are interested in these features, please reach out to the developers.
```

#### `solver`

:Parameters:
:`name` (`str`, default = `highs`): The solver to use for the optimization problem. If not set, the default solver (currently [HiGHS](https://highs.dev/)) is used.
:`log` (`bool`, default = `true`): Whether to log the solver output to a file.
:`attributes` (`dict`, optional): Additional attributes to pass to the solver.

```{code-block} yaml
:caption: Example for the `solver` section.

config:
  optimization:
    solver:
      name: highs
      log: false
      attributes:
        solver: ipm
```

#### `snapshots`

Here we define the Snapshots (IESopt's representation of time steps, including auxiliary information).

:Parameters:
:`count` (`int`): The number of Snapshots to use in the optimization.
:`names` (`str`, optional): Linked column of a loaded file (using the usual `col@file` syntax) that contains the names of the Snapshots. These are purely for aesthetic purposes (e.g., result data frames) and are not used in the optimization.
:`weights` (`float`, default = `1`): The duration of each Snapshot in hours. Values below `1` are interpreted as fractions of an hour, e.g., `0.25` for 15 minutes.
:`offset` (`int`, default = `0`): The offset at where to start reading a time series passed to the model. `168` means that the first 168 entries (rows) will be skipped and the first Snapshot is based on the 169th row.
:`offset_virtual_files` (`bool`): Mandatory if `offset > 0`, without effect otherwise. If `true` time series passed using the `virtual_files` keyword argument will respect the `offset`, otherwise they are considered to "be already offset" and will be used directly from the first row on.

```{code-block} yaml
:caption: Example for the `snapshots` section, with non-1-hourly resolution.

config:
  optimization:
    snapshots:
      count: 24   # total of four days modeling period
      weights: 4  # four hours per Snapshot
      offset: 6   # start at the second day
```

#### `objectives`

```{caution}
This setting is part of advanced functionality. It is not fully documented, or may be partially broken in any given release. If you are interested in this feature, please reach out to the developers.
```

This allows defining custom objective expressions for the optimization problem. This can be useful if you want to optimize for a specific objective that is not directly supported by IESopt. Per default, IESopt is optimizing the only base objective expression, which is the model's total cost (called `total_cost`).

```{code-block} yaml
:caption: Example for the `objectives` section.

config:
  optimization:
    objectives:
      emissions: [co2_emissions.exp.value]
```

The above constructs a new objective expression that only consists of `co2_emissions.exp.value`. It may also be initialized empty (`[]`), in which case you can add terms later on in the model definition.

#### `multiobjective`

```{caution}
This setting is part of advanced functionality. It is not fully documented, or may be partially broken in any given release. If you are interested in this feature, please reach out to the developers.
```

:Parameters:
:`mode` (`str`): The mode to use for multi-objective optimization, currently supported modes are: `EpsilonConstraint`, `Lexicographic`, `Hierarchical`.
:`terms` (`list[str]`): A list of objectives to optimize.
:`settings` (`dict`): Settings for the multi-objective optimization, refer to the documentation of [MultiObjectiveAlgorithms.jl](https://github.com/jump-dev/MultiObjectiveAlgorithms.jl) for more information.

```{code-block} yaml
:caption: Example for the `multiobjective` section.

config:
  optimization:
    multiobjective:
      mode: EpsilonConstraint
      terms: [total_cost, emissions]
      settings:
        MOA.SolutionLimit: 5
```

```{note}
Refer to the related example models for more information on how to use multi-objective optimization in IESopt.
```

#### `soft_constraints`

This was called `constraint_safety` in all versions previous to `v2.0.0`. It controls if and how certain constraints of the model are relaxed to allow penalized violation of said constraints. This can be helpful, e.g., if your model is infeasible for certain external settings and you might want to ensure getting an approximate solution.

```{code-block} yaml
:caption: Example for the `soft_constraints` section.

config:
  optimization:
    soft_constraints:
      active: true
      penalty: 1e6
```

:Parameters:
:`active` (`bool`, default = `false`): Activate the feature.
:`penalty` (`float`): Penalty that is used to penalize constraint violations.

### `files`

This can be used to define input files that are later referenced in the configuration file. Each filename (possibly including a path) is linked to a name that can be used to reference the file later on.

```{code-block} yaml
:caption: Example for the `files` section.

config:
  files:
    data: inputs_2023_base.csv
```

In the above example, the file `inputs_2023_base.csv` is linked to the name `data`. This means that the file can be referenced in the configuration file using `data`, accessing a column - e.g., "pv_generation" - using `pv_generation@data`.

:::{note}
Assuming that, in the above example, we call `data` the file's "descriptor" and `inputs_2023_base.csv` the file's "name", then make sure that **the descriptor does not start with an underscore**, and further only uses alphanumeric characters and underscores (so no `!`, `~`, or other "unexpected" special characters).
:::

#### `_csv_config`

:::{caution}
This feature is experimental and can change, break, or be discontinued at any time.
:::

You can configure the behavior of the CSV reader by adding a `_csv_config` section to the `files` section.

:Parameters:
:`comment` (`string`, default = `null`): If empty/not-given, no "comments" are recognized. If set to any string, all lines starting with this string are considered comments and ignored. Common options are `#` or `;`. Make sure to properly escape the string if needed, e.g., `comment: "#"`.
:`delim` (`char`, default = `,`): The delimiter used in the CSV file. Common options are `,` (EN locale), `;` (DE locale), or `\t` (tab-separated).
:`decimal` (`char`, default = `.`): The decimal separator used in the CSV file. Common options are `.` (EN locale) or `,` (DE locale). Make sure this is set correctly in conjunction with the `delim` setting.

```{code-block} yaml
:caption: Ignore comment rows in input CSVs.

config:
  files:
    _csv_config:
      comment: "#"
```

```{code-block} yaml
:caption: Switch to a format often used on German systems.

config:
  files:
    _csv_config:
      delim: ";"
      decimal: ","
```

### `results`

Settings for the results output. Details to be added.

:Parameters:
:`enabled` (`string`, default = `all`): Controls the mode of automatic result extraction. If this is set to `none`, no results will be read from the solver after optimizing the model - you can however still access the solver results directly, see for example {py:func}`iesopt.jump_value`. If set to `reduced`, all primal results, as well as shadow prices for all `Node`s will be extracted; this is a good compromise between speed and usability and skips the extraction of results that are often not needed.
:`memory_only` (`bool`, default = `true`): Whether to store the results in memory only, without writing them to disk. This can be useful if you plan to access and further process the results directly in Python or Julia, or only want to store specific results.
:`compress` (`bool`, default = `false`): Whether to compress the results when writing them to disk. This can save disk space but might increase the time needed to write and read the results. Refer to [JLD2.jl](https://github.com/JuliaIO/JLD2.jl) for more information about compression.
:`include` (`str`, default = `none` or `input+log`): A list of result extraction modes to activate, see below for more details. The default depends on the setting of `memory_only`: If `memory_only` is `true`, the default is `none`, otherwise it is `input+log`. You can use `all` to activate all possible settings.
:`backend` (`str`, default = `jld2`): Backend to use in the result extraction. Currently `jld2` is the main/working one, while we are trying to improve the `duckdb` backend.

```{code-block} yaml
:caption: Example for the `results` section.

config:
  results:
    enabled: reduced
    memory_only: true
```

```{admonition} Details: Result extraction modes
Currently the following options exist for the `include` setting:

:`input`: Add information about the model's input data to the results.
:`git`: Add information about the status of any git setup that exists in the model's folder.
:`log`: Add IESopt's full log of the optimization run to the results.

These modes can be combined using `+`. For example, `input+git` will include both the input data and the git information in the results. If `include` is set to `all`, all modes are included. If `include` is set to `none`, no modes are included.
```

```{note}
Refer to the [name](#name) section for information on how the model and scenario names are used in the results output.
```

### `paths`

This section as a whole, or the individual paths, are optional - defaults will be used for those not set.

:Parameters:
:`files` (`str`, default = `./files/`): The path to the directory where input files are stored.
:`templates` (`str`, default = `./templates/`): The path to the directory where templates are stored.
:`components` (`str`, default = `./model/`): The path to the directory where model topology files are stored. These allow loading a large number of components at once. Refer to the [components](#components) section for more information.
:`addons` (`str`, default = `./addons/`): The path to the directory where addons (`*.jl` files) are stored.
:`results` (`str`, default = `./out/`): The path to the directory where results should be stored.

```{code-block} yaml
:caption: Example for the `paths` section.

config:
  paths:
    files: data/
    templates: templates/
    components: model/
    results: out/
```

```{note}
The paths are all relative to the location of the top-level configuration file.
```

## `addons`

Additional settings for specific addons.

```{code-block} yaml
:caption: Example for the `addons` section in the top-level YAML configuration file.

addons:
  ModifyHeatStorages:
    alpha: 0.93
    temperature: 60.0
```

```{note}
This section is optional and only needed if you want to use addons. The settings for the addons are specific to the addon.
```

## `carriers`

Definition of all energy carriers.

```{code-block} yaml
:caption: Example for the `carriers` section in the top-level YAML configuration file.

carriers:
  electricity: {}
  co2: {}
```

## `components`

This is the main section where all model components are defined (or loaded). There are two possibilities to define components: `components` and `load_components`. The former is used to define components directly in the top-level configuration file, while the latter is used to load components from a file. At least one of these sections must be present in the top-level configuration file - both can be used at the same time.

```{code-block} yaml
:caption: Basic example for the `components` section.

components:
  main_grid_node:
    type: Node
    carrier: electricity
```

When using `load_components`, the easiest way is to pass a list of filenames. These files are then loaded from the `components` path (see the [paths](#paths) section) and the components are added to the model. Note that using `components` is not necessary when using `load_components`, and is only done here for demonstration purposes.

```{code-block} yaml
:caption: Advanced example, utilizing `load_components`.

load_components:
  - units.csv
  - nodes.csv
  - profiles.csv

components:
  co2_emissions:
    type: Profile
    carrier: co2
    mode: destroy
    node_from: total_co2
    cost: 100
```

`````{note}
The `load_components` section allows more complex ways to read components from files: You can pass `.csv` as sole list entry to load all CSV files in the `components` path, or you can pass one, or multiple, regex patterns as list entries to load only specific files. For example, using

```{code-block} yaml
load_components:
  - ^09[/\\]((?!snapshots\.csv$).)*\.csv$
```

will load all CSV files in the `components` path that are in a subfolder `09` except for `snapshots.csv`.

**Note:** It is recommended to use `[/\\]` as path separators, like in the regex above, so the model can work on both UNIX and Windows systems.
`````
