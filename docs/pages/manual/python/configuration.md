# Configuration

Various configuration options are handled using environment variables. These can easily be configured using `.env` files. You can check out [`python-dotenv`](https://pypi.org/project/python-dotenv/) for more information on how to use `.env` files with Python.

**How to?** For the basics, create a file called `.env` in the root of your project and add the following:

```{code-block} text
:caption: A simple `.env` file.

IESOPT_CORE = 2.0.0
```

:::{tip}
For many applications it is perfectly fine not to use any configuration at all. The defaults are chosen to work well in most cases. Each release of the Python wrapper `iesopt` is bound to a specific version of the Julia package `IESopt.jl`. Changing this is only necessary if you want to use a different version of the Julia package. Further, we install a default version of `HiGHS` as solver - so unless you need to use (and have access to) a commercial solver, you should be fine with the default settings.
:::

## Julia packages

## IESopt.jl

To install a specific version of the Julia core, IESopt.jl, use the following:

```{code-block} text
:caption: Setting the IESopt.jl version.

IESOPT_CORE = 2.0.0
```

## Solvers

Installing solver packages can be done using the following:

```{code-block} text
:caption: Setting the solver versions.

IESOPT_SOLVER_HIGHS = 1.12.0
```

Other examples may be setting `IESOPT_SOLVER_CPLEX` or `IESOPT_SOLVER_GUROBI`.

### Forcing a solver executable version

For example when installing Gurobi, it might be that the Julia wrapper pulls a version newer than the one you are able
to use according to your license. This can be fixed by explicitly adding the corresponding `_jll` ("binary wrapper")
as dependency:

```{code-block} text
:caption: Fixing a solver executable version in `.env`.

IESOPT_PKG_Gurobi_jll = 11.0.3
IESOPT_SOLVER_GUROBI = 1.6.0
```

This will use the latest `Gurobi_jll` version related to Gurobi 11.

## Important versions

The following other entries are potentially used in some projects:

```{code-block} text
:caption: Fine grained version control.

IESOPT_JULIA = 1.11.1
IESOPT_JUMP = 1.23.3
```

## Arbitrary packages

To install packages that are not part of or related to IESopt, you can use the following:

```{code-block} text
:caption: Arbitrary packages.

IESOPT_PKG_ModelingToolkit = 1.0.3
```

Make sure the proper casing of the package name is used. The package name is case-sensitive. Even though environment variables are commonly upper-case only, the package name has to reflect the Julia package's wording.

## Non-registered packages

To install non-registered packages, you can use the following syntax:

```{code-block} text
:caption: Installing packages from GitHub.

IESOPT_CORE = https://github.com/ait-energy/IESopt.jl#super-important-feature
```

When such a repository is updated, we might not be able to automatically update the package. In this case, you can use the following

```{code-block} python
:caption: Updating packages from GitHub.

import iesopt
iesopt.julia.seval('import Pkg; Pkg.update("IESopt")')
```

to forcefully update a Julia package.

## Options

Currently the following options are available:

:Options:
:`IESOPT_MULTITHREADED`: `yes` or `no` (default). Talk to us before using this.
:`IESOPT_OPTIMIZATION`: `rapid`, `latency` (default), `normal`, or `performance`. Consider using `latency` for small models, or repeatedly executing your code, since it may be faster for these kind of work loads. Set it to `performance` for large models where initial up-front costs are not relevant. `normal` refers to the default settings chosen by "just launching Julia". For iterative development on a single small model, `rapid` might be the best choice - however, it compromises actual performance, even in subsequent runs, so it is not recommended for production code.
