# Updating

This page collects information about updating the project between specific versions.

## 1.x.y to 2.0.0

The `2.0.0` release follows the breaking change of `IESopt.jl` going to `v2.0.0`. This was mainly triggered by a proper rework of how addons work, including a new internal handling for more complex expressions (allowing more flexibility in configuring `conversion`, or `cost` settings), as well as better support around templates (e.g. the introduction of `Virtual`s). A few breaking changes that were planned for quite some time are part of this.

### Changes to the top-level config

To be written: everything.

### Changes to keyword arguments

To be written: "parameters" and "config".

### Changes to result extraction

We saw increasing interest in actively "filtering" results of various models. This triggered the implementation of a new result backend (initially only JLD2) supported by DuckDB. This is (as of 2.0.0) not enabled as default, since it does not fully support the functionality that the Python wrapper `iesopt` provides. However, we plan on switching to this backend in the future.

### Changes to addons

To be written: Link to addon page/docs as soon as they are done.

### Changes to examples, and more

Everything that was previously part of `IESoptLib.jl` is now integrated into `IESopt.jl`. Functionality around this can be accessed using `IESopt.Assets`.

### Other changes

#### Tags

To be written.
