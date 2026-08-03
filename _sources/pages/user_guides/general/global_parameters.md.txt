# Global parameters

Global parameters are those that are accessible from the outside of the model. They are defined in the `parameters`
section of the top-level configuration file.

## Formats

A few different formats are possible to define global parameters.

### Basic dictionary

```{code-block} yaml
:caption: Using a basic dictionary.

parameters:
  total_demand: 100
  total_supply: ~

config:
  # everything else ...
```

Here, the `~` character is used to indicate a "null value" (= `None` in Python) --- another common way would be to use
`null`. The `total_supply` parameter does not have a (default) value, so it has to be set from the outside if it is
actually used in the model. On the other hand, the `total_demand` parameter has a default value of `100` --- this can,
but does not have to, be overwritten from the outside.

### An external file

This requires a file in the same directory as the configuration file, with the name `global.iesopt.param.yaml`:

```{code-block} yaml
:caption: `global.iesopt.param.yaml`

total_demand: 100
total_supply: ~
```

Then the top-level configuration file can be simplified to:

```{code-block} yaml
:caption: `config.iesopt.yaml`

parameters: global.iesopt.param.yaml
  
config:
  # everything else ...
```

Note that starting with core `v2.7.0` the file extension can be omitted:

```{code-block} yaml
:caption: `config.iesopt.yaml`

parameters: global
  
config:
  # everything else ...
```

### Multiple external files

Consider a second parameter file, `heat.iesopt.param.yaml`, that contains, e.g., all heat related parameters:

```{code-block} yaml
:caption: `heat.iesopt.param.yaml`

heat_temperature: 80
```

Then the top-level configuration file can be extended to include both files (again making use of the possibility to omit
the file extension):

```{code-block} yaml
:caption: `config.iesopt.yaml`

parameters:
  - global
  - heat

config:
  # everything else ...
```

:::{caution}
This will fail if the entries in the different files are not unique.
:::

## A folder for all parameters

Especially when using multiple parameter files, it can be useful to have a dedicated folder for all these --- otherwise
the model's root directory can quickly become cluttered. This can be done by specifying a folder in the top-level
config's `paths` section, similar to how it works for other file types:

```{code-block} yaml
:caption: `config.iesopt.yaml`

parameters:
  - default
  - increase_demand
  - cold_weather

config:
  # ... other config options ...
  paths:
    parameters: params/

carriers:
  # ... all the carriers ...

components:
  # ... all the components ...
```

This, as an example, will now look for the parameter files in the `params/` folder (you could name that `options`, or
`data/parameters`, or anything you need) --- as always, relative to the location of the top-level config file. 

## Overwriting parameters

Sometimes it can be quite useful to overwrite parameters, when using multiple files. Consider the same files as above,
with a new file that can be slotted in to overwrite (increase) the `total_demand` parameter:

```{code-block} yaml
:caption: `high_demand.iesopt.param.yaml`

total_demand: 200
```

Then the top-level configuration file can be extended to include all three files --- only when explicitly allowing that
parameters can be overwritten:

```{code-block} yaml
:caption: `config.iesopt.yaml`

parameters:
  - global
  - heat
  - high_demand

config:
  general:
    # ...
    parameters:
      mode: overwrite  # This otherwise defaults to `unique`.
  
  # ...
```

### Python: Toggle overwriting

If you want to programmatically control the overwriting of parameters from Python, you can do so by directly setting the
corresponding configuration option, like this:

```{code-block} python
:caption: Modifying the `config` section using Python.

import iesopt

model = iesopt.run("config.iesopt.yaml", config = {"general.parameters.mode": "overwrite"})
```

Refer to the [user guide on the `config` keyword argument](./kwargs_config.md) for more details on how this works.

## Python: Accessing parameters

When using the `iesopt` Python package, parameters can be set from the outside. This can be very helpful to
programmatically control various aspects of the model.

### Basic dictionary

For the basic style, using the following top-level configuration file:

```{code-block} yaml
:caption: Using a basic dictionary.

parameters:
  total_demand: 100
  total_supply: ~

config:
  # everything else ...
```

The parameters can be set from Python as follows:

```{code-block} python
:caption: Basic Python script.

import iesopt

model = iesopt.run("config.iesopt.yaml", parameters = dict(total_supply=150))
```

:::{tip}
Above, we used `dict(total_supply=150)` to create a dictionary. This is equivalent to `{"total_supply": 150}`.
:::

If you are not using `iesopt.run(...)` to run the model, then pass the parameters to the initial `iesopt.Model(...)`
call like this:

```{code-block} python
:caption: Basic Python script.

import iesopt

model = iesopt.Model("config.iesopt.yaml", parameters = dict(total_supply=150))
model.generate()
model.optimize()
```

### An external file

Overwriting parameters from an external file is also possible --- and works exactly the same way as above. Consider that
you specified the parameters in a file called `global.iesopt.param.yaml`, then the same Python calls as above can be
used.

However, lets say you have a second parameter file, called `future.iesopt.param.yaml`, that contains slightly different
values for the parameters. Let's say you want to default to the `global.iesopt.param.yaml` file --- which you can do by
specifying it in the top-level configuration file:

```{code-block} yaml
:caption: `config.iesopt.yaml`

parameters: global
  
config:
  # everything else ...
```

If you want, e.g., for a specific run / scenario / etc., to use the `future.iesopt.param.yaml` file instead, you can
simply specify it in the `iesopt.run(...)` call:

```{code-block} python
:caption: Basic Python script.

import iesopt

model = iesopt.run("config.iesopt.yaml", parameters = "future")
```

### Multiple external files

Finally, if you want to use multiple files (e.g., to structure your parameters), you can control these from Python as
well. Let's assume you have two base parameter files:

```{code-block} yaml
:caption: `current.iesopt.param.yaml`

total_demand: 100
total_supply: 100
```

```{code-block} yaml
:caption: `future.iesopt.param.yaml`

total_demand: 100
total_supply: 150
```

And a third file that can be used to overwrite the `total_demand` parameter:

```{code-block} yaml
:caption: `high_demand.iesopt.param.yaml`

total_demand: 200
```

Make sure to allow parameter overwriting in the top-level configuration file, e.g., with the following basic (default)
setup:

```{code-block} yaml
:caption: `config.iesopt.yaml`

parameters: current

config:
  general:
    # ...
    parameters:
      mode: overwrite  # This otherwise defaults to `unique`.
  
  # ...
```

Then you can run different models with the following Python code:

```{code-block} python
:caption: Basic Python script.

import iesopt


model_current = iesopt.run(
    "config.iesopt.yaml"
)

model_future = iesopt.run(
    "config.iesopt.yaml",
    parameters = "future"
)

model_high = iesopt.run(
    "config.iesopt.yaml",
    parameters = ["current", "high_demand"]
)

model_future_high = iesopt.run(
    "config.iesopt.yaml",
    parameters = ["future", "high_demand"]
)
```

### Overwriting external parameters

Until now we only discussed how to overwrite parameters from the outside when using the basic dictionary style and how
to control which external files are loaded. However, it is also possible to overwrite parameters from the outside when
using external files. This can be done by passing the override-dictionary as last entry in the list of parameters:

```{code-block} python
:caption: Basic Python script.

import iesopt

model = iesopt.run(
    "config.iesopt.yaml",
    parameters = ["future", "high_demand", dict(total_supply=75)]
)
```
