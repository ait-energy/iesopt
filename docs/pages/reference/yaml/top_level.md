# Top-level

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

General global parameters, that the whole model can access. Can be set from outside when, e.g., when calling {py:func}`iesopt.run`. See the [global parameters](./global_parameters.md) section for more details.

```{code-block} yaml
:caption: Example for the `parameters` section in the top-level YAML configuration file.

parameters: global_params_scenarioHIGH.iesopt.param.yaml
```

```{note}
This section is optional and only needed if you want to global model parameters.
```

## `config`

General configuration settings for the optimization model.

```{code-block} yaml
:caption: Example for the `config` section in the top-level YAML configuration file.

config:
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

### `name`

- `model`
- `scenario`

---

### `optimization`

#### `problem_type`

:Options:
:`LP`: Restricted to (continuous) linear programming formulations.
:`MILP`: Enables mixed-integer linear programming formulations.

```{code-block} yaml
:caption: Example for the `problem_type` section.

config:
  optimization:
    problem_type: LP
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

```{code-block} yaml
:caption: Example for the `snapshots` section.

config:
  optimization:
    snapshots:
      count: 24
      weights: 4
```

### `files`

This can be used to define input files that are later referenced in the configuration file. Each filename (possibly including a path) is linked to a name that can be used to reference the file later on.

```{code-block} yaml
:caption: Example for the `files` section.

config:
  files:
    data: inputs_2023_base.csv
```

In the above example, the file `inputs_2023_base.csv` is linked to the name `data`. This means that the file can be referenced in the configuration file using `data`, accessing a column - e.g., "pv_generation" - using `pv_generation@data`.

### `results`

Settings for the results output. Details to be added.

- `enabled`
- `memory_only`
- `compress`
- `include`

```{code-block} yaml
:caption: Example for the `results` section.

config:
  results:
    enabled: true
    memory_only: true
```

### `paths`

This section as a whole, or the individual paths, are optional and the following defaults are used if not set:

- `files`: `./files/`
- `templates`: `./templates/`
- `components`: `./model/`
- `addons`: `./addons/`
- `results`: `./out/`

```{note}
The paths are all relative to the location of the top-level configuration file.
```

```{code-block} yaml
:caption: Example for the `paths` section.

config:
  paths:
    files: data/
    templates: templates/
    components: model/
    results: out/
```

#### `files`

The path to the directory where input files are stored.

#### `templates`

The path to the directory where templates are stored.

#### `components`

The path to the directory where model topology files are stored. These allow loading a large number of components at once.

#### `addons`

The path to the directory where addons (`*.jl` files) are stored.

#### `results`

The path to the directory where results should be stored.

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

This is the main section where all model components are defined (or loaded). Details to be added.
