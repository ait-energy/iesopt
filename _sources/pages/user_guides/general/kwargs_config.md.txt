# Python: Modify `config`

This covers how the top-level configuration file can be modified using the `config` keyword argument, directly when
running the model.

Consider a rolling optimization use-case, where the model is run multiple times --- each time a different offset across
the time horizon is used. This may be the base for a model-predictive-control approach or a myopic foresight model. The
top-level configuration file could look like this:

```{code-block} yaml
:caption: `config.iesopt.yaml`

parameters: global

config:
  general:
    version: 2.7.0
  optimization:
    problem_type: LP
    snapshots:
      offset: 0
      count: 24

carriers:
  # ... all the carriers ...

components:
  # ... all the components ...
```

Now, let's assume you want to run that model in a `for` loop, where the `offset` is changed each time. You can
simply pass the new value of `offset` to the `config` keyword argument, like this:

```{code-block} python
:caption: Rolling optimization using Python.

import iesopt

for day in range(0, 365):
    model = iesopt.run(
        "config.iesopt.yaml",
        config = {
            "optimization.snapshots.offset": day * 24,
        }
    )

    # ... do something with the results here ...
```

As you can see, you can access any entry in the configuration file using a "dot notation".

Modifying this to feature a longer look-ahead horizon (than the step size) could then also be done from Python, by
simply adding a second entry to the `config` dictionary:

```{code-block} python
:caption: Rolling optimization with a one-week window.

import iesopt

for day in range(0, 365):
    model = iesopt.run(
        "config.iesopt.yaml",
        config = {
            "optimization.snapshots.offset": day * 24,
            "optimization.snapshots.count": 168,
        }
    )

    # ... do something with the results here ...
```

:::{tip}
You can use this to easily control which input data files are loaded --- without the need to manually introduce a
parameter that controls each file's name. Just use the `config` keyword argument to set, for example, that the file
registered as `data` (see example [config](https://ait-energy.github.io/iesopt/pages/user_guides/general/monte_carlo.html#modifying-the-config)) points to a specific weather year's file, by passing `config = {"files.data": "weather_res_2023.csv"}`.
:::
