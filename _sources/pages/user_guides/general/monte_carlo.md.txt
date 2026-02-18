# Monte Carlo simulations

This covers a few different ways of interacting with / controlling an IESopt model from Python. While it is explained on
the example of a simple Monte Carlo simulation, the same principles apply to other (similar) use-cases as well.

We cover two common needs, encountered when running the same model multiple times:

1. Modifying a scalar parameter, e.g., the fixed CO$_2$ price.
2. Modifying a time series, e.g., the electricity price or a renewable generator's availability.

## Using a parameter

Consider the following top-level configuration file:

```{code-block} yaml
:caption: `config.iesopt.yaml`

parameters:
  gas_eur_mwh: 27.5
  res_file: data_res_2017

config:
  # ... other config options ...
  files:
    data: <res_file>.csv

carriers:
  # ... all the carriers ...

components:
  # ... all the components ...
```

This can then be controlled from Python, by passing parameters to the `iesopt.run(...)` function --- refer to the
[user guide on the global parameters](./global_parameters.md) for more information on this:

```{code-block} python
:caption: Running a Monte Carlo simulation using Python.

import random
import iesopt


for _ in range(1000):
    gas_price = random.uniform(20, 40)
    weather_year = random.randint(2017, 2022)

    model = iesopt.run(
        "config.iesopt.yaml",
        parameters = dict(
            gas_eur_mwh = gas_price,
            res_file = f"data_res_{weather_year}",
        )
    )

    # ... do something with the results here ...
```

## Modifying the `config`

A simpler way --- especially when modifying multiple files at the same time --- is to make use of the `config` keyword.
We now omit the `res_file` parameter from the top-level configuration file, e.g., modifying it to:

```{code-block} yaml
:caption: `config.iesopt.yaml`

parameters:
  gas_eur_mwh: 27.5

config:
  # ... other config options ...
  files:
    data: data_res_default.csv

# ... everything else ...
```

Then, the `iesopt.run(...)` function can be called with a `config` keyword argument, which is a dictionary containing
the new values for the configuration. This dictionary can contain any entry in the configuration file, using a "dot
notation" to access the nested entries. The above Python example can then be modified to:

```{code-block} python
:caption: Running a Monte Carlo simulation using Python.

import random
import iesopt


for _ in range(1000):
    gas_price = random.uniform(20, 40)
    weather_year = random.randint(2017, 2022)

    model = iesopt.run(
        "config.iesopt.yaml",
        parameters = dict(gas_eur_mwh = gas_price),
        config = {
            "files.data": f"data_res_{weather_year}.csv",
        }
    )

    # ... do something with the results here ...
```

Refer to the [user guide on the `config` keyword argument](./kwargs_config.md) for more details on how this works and
what it can be used for.

## Using a `pd.DataFrame`

Often, the previous approaches comes at an unnecessary overhead: First, writing some data from the Python script to a
CSV file, to then read it back in again in IESopt. This can be avoided by directly passing a `pd.DataFrame` to the
`iesopt.run(...)` function. Consider the same top-level configuration file as above, as well as a function
`prepare_weather_data` that is assumed to return a `pd.DataFrame` for a given year, then the Python script can be
modified to:

```{code-block} python
:caption: Running a Monte Carlo simulation using Python.

import random
import iesopt


dfs_weather = {y: prepare_weather_data(y) for y in range(2017, 2023)}

for _ in range(1000):
    gas_price = random.uniform(20, 40)
    weather_year = random.randint(2017, 2022)

    model = iesopt.run(
        "config.iesopt.yaml",
        parameters = dict(gas_eur_mwh = gas_price),
        virtual_files = dict(data = dfs_weather[weather_year])
    )

    # ... do something with the results here ...
```

This will randomly select a weather year from 2017 to 2022, and use the corresponding `pd.DataFrame` as the input
data --- directly passing it to the Julia core model, without any intermediate CSV file.
