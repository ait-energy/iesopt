# Top-level

The top-level YAML configuration file, often named `config.iesopt.yaml`, is the main configuration file for the IESopt optimization model. It may contain the following main sections:

1. `parameters`: General global parameters.
2. `config`: General configuration settings for the optimization model.
3. `addons`: Additional settings for specific features or plugins.
4. `carriers`: Definitions of energy carriers.
5. `components` (and/or `load_components`): Definitions of core components.

```{note} As mentioned in the [intro section](./index.md) of the YAML reference, dictionaries are considered to not guarantee order. Therefore, the order of the sections in the YAML file is not important - however, the order given above is recommended for readability.
```

## `parameters`

General global parameters, that the whole model can access. Can be set from outside when, e.g., when calling {py:func}`iesopt.run`. See the [global parameters](./global_parameters.md) section for more details.

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

### `optimization`

- `problem_type`
- `solver`
- `snapshots`

### `files`

### `results`

- `enabled`
- `memory_only`
- `compress`
- `include`

### `paths`

- `files`
- `templates`
- `components`
- `results`

## `addons`

## `carriers`

## `components`
