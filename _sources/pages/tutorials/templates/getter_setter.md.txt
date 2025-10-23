# Getter and setter functions

Templates offer different getter and setter functions to access and modify their parameters. These functions are mainly
used in the `validate(...)` and `prepare(...)` functions.

We consider the following example template in all following sections:

```{code-block} yaml
:caption: `SampleGroup.iesopt.template.yaml`

parameters:
  bess_size: ~
  cop_default: heatpump_cop_gs@default_data
  _internal_cop: ~

functions:
  validate: |
    # ... some code here ...
  prepare: |
    # ... some code here ...
  finalize: |
    # ... some code here ...

components:
  # ... all the actual components ...
```

:::{tip}
Setting a parameter to `~` per default is a concise way of setting it to `null` (the YAML equivalent of `None` in
Python).
:::

## Validating parameters (`get`, `get_ts`)

To validate a parameter, you can get its value using the `get(...)` function:

```{code-block} yaml
:caption: `validate` function.

functions:
  validate: |
    @check this.get("bess_size") >= 0
    @check all(this.get_ts("cop_default") .>= 0)
```

First, `this.get(...)` requires the name of the parameter you want to access. The `@check` macro is used to streamline
parameter validation across different templates (e.g., making sure that reasonable errors are raised when not passing
the check). So, `this.get("bess_size")` returns the value of the `bess_size` parameter; it is then checked to be
non-negative.

The second line shows how to access a time series parameter using the `get_ts(...)` function. Here, this
will return the time series that the `cop_default` parameter points to (when not modified from the outside, this points
to the column `heatpump_cop_gs` in the `default_data` file). The, maybe unfamiliar, comparison operator `.>=` is used to
compare the complete time series to `0`, "vectorizing" the comparison (= comparing every entry against `0`). Since this
returns a `Vector` (similar to a `list` in Python) of boolean values, we make use of the `all(...)` function that will
only return `true` if all entries are `true`. 

## Setting a parameter (`set`)

To set a parameter, you can use the `set(...)` function. This function takes the name of the parameter you want to set,
and the new value you want to set it to. Let's double the value of the `bess_size` parameter:

```{code-block} yaml
:caption: `prepare` function.

functions:
  prepare: |
    this.set("bess_size", this.get("bess_size") * 2)
```

## Setting a time series target (`set`)

If now intend to set the internal (private) parameter `_internal_cop`, that is used somewhere in the template's
components, to point to the same time series as specified by the `cop_default` parameter, we can do so using the
`set(...)` function:

```{code-block} yaml
:caption: `prepare` function.

functions:
  prepare: |
    this.set("_internal_cop", this.get_ts("cop_default"))
```

This will set the `_internal_cop` parameter to contain, e.g., the string `heatpump_cop_gs@default_data`, so again
pointing to the column `heatpump_cop_gs` in the `default_data` file.

## Modifying a time series (`set_ts`)

However, you most likely want to also modify the time series that is used in the template. This can be done using the
`set_ts(...)` function. This function takes the name of the time series you want to modify, and the new value you want
to set it to. The new value can be a single (scalar) value, or a time series:

```{code-block} yaml
:caption: `prepare` function.

functions:
  prepare: |
    # Applying a 5% loss to the COP.
    cop = this.get_ts("cop_default") .* 0.95

    this.set("_internal_cop", "real_cop@internal_data")
    this.set_ts("_internal_cop", cop)
```

First, this calculates a new time series `cop`, including some losses. Then, we make sure to set the parameter
`_internal_cop`, so that it points to a new time series specified in column `real_cop` in the `internal_data` file.
Note that `internal_data` may or may not already exist: If it does, the column `real_cop` will be inserted or
overwritten; if it does not exist, a new "file" (just a table in memory) will be created, that can be referenced across
the model using `column_name@internal_data`, and the column `real_cop` will be created inside it.

Then we can make use of the `set_ts(...)` function --- in comparison to the `set(...)` function, this will not modify
the parameter `_internal_cop`, but the time series that it points to. This means that the column `real_cop` in the
`internal_data` file will be modified to contain the new time series `cop`.

Alternatively, you can also call it as `this.set_ts("other_col@other_file", value)`, if you want to directly access a
specific column in a specific file (without using a parameter that points to it).

:::{caution}
As is the case in Python, e.g., when working with `pandas` dataframes, the "files" that IESopt keeps in memory are 
"shared" across different accessors. Think about a dataframe `df`. If you do `df_other = df` and then modify
`df_other["col"] = 42`, the column `col` in `df` will also be modified to contain the value `42`. This is because both
`df` and `df_other` point to the same object in memory. The same is true for the files in IESopt. This entails that
modifying `real_cop@internal_data` in a template will lead to all components instantiated from that template to access
the same time series. While this can be useful when actually sharing data across components, it can also lead to
unexpected behavior when not intended. So be careful when using the `set_ts(...)` function.
:::

## Unique time series

To prevent the above pitfall, you can create a unique entry in a certain file, e.g., by making use of the name that the
template is instantiated with. Since we require all components to have a unique name, this will guarantee that each
component instantiated from the same template will have its own copy of the time series. This can be done using:

```{code-block} yaml
:caption: `prepare` function.

functions:
  prepare: |
    # Applying a 5% loss to the COP.
    cop = this.get_ts("cop_default") .* 0.95

    # Construct a file name that is unique to this component.
    this.set("_internal_cop", "real_cop@$(this.name)_data")

    # Set the time series to the new value.
    this.set_ts("_internal_cop", cop)
```

Let's see what we've done here. First, `this.name` will return the name of the component that is being instantiated from
the current template. This is the name that is used to identify the component in the model.

Next, we note that string interpolation makes use of the `$(...)` syntax in Julia. Drawing a parallel to Python, writing
`"real_cop@$(this.name)_data"` would be equivalent to writing `f"real_cop@{this.name}_data"` in Python when using
f-strings.

This means that each component will now register a unique file. Let's assume that the component is called `group_01`.
Then, the file will be called `group_01_data`. Writing a time series into the column `real_cop` can now never lead to
conflicts with other components. Further calculations or time series in the same template could then make use of 
additional columns, e.g., `availability@$(this.name)_data`.

:::{tip}
You can also use `"real_cop@" * this.name * "_data"`, which is equivalent to `"real_cop@" + this.name + "_data"`. While
Julia has a really interesting reason for using `*` for string concatenation --- linked to the fact that `+` typically
implies a commutative behavior that string concatenation does not have (cf. the
[Julia documentation](https://docs.julialang.org/en/v1/manual/strings/#man-concatenation)) --- most people unfamiliar
with Julia will most likely find the `*` operator confusing. We therefore recommend to not using string concatenation
using `*` at all.
:::


