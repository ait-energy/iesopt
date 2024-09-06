# Integrated Energy System Optimization

:::{admonition} _IESopt -- an Integrated Energy System Optimization framework._
:class: tip

IESopt is developed and maintained at the Center for Energy at AIT Austrian Institute of Technology GmbH. The framework isdesigned to support the optimization of energy systems that are characterized by a high degree of integration between different energy carriers and sectors. It focuses on offering a modular and adaptable tool for modelers, that does not compromise on performance, while still being user-friendly. This is enabled by reducing energy system assets to abstract building blocks, that are supported by specialized implementation, and can be combined into complex systems without the need of a detailed understanding of mathematical modeling or proficiency in any coding-language.
:::

:::{caution}
The documentation is currently being put together based on cleaned parts of the internal docs. Until this is finished, this documentation only contains some placeholders.
:::

## Overview

This overview of `iesopt`'s documentation [^diataxis] will help you know where to find what you are looking for.

### Getting started

1. The {ref}`Installation` section explains how to quickly install and set up `iesopt`.
2. If you are new, you can then work through {ref}`A first model`, which will guide you through all the basics you need
to now.

### Using this documentation

For anything beyond {Getting started}`Getting started`, the following provides a high-level overview of the remaining
documentation that can be helpful when creating your own models:

1. **Tutorials** will help you learn how to apply `iesopt`'s various main functionalities, to solve energy
system optimization models. Start here if you are new and have completed the {ref}`A first model` initial tutorial.
2. **User guides** provide various concise how-to guides, that help you accomplish a certain task, correctly
and safely. Consult these to remind yourself _how to do X_.
3. **Reference** contains technical reference for `IESopt.jl` core components, the YAML syntax, APIs, and more
internal details. It assumes that you already have a basic understanding of the core concepts of `iesopt`.
4. **Developer documentation** can be consulted for tips on how to improve `iesopt`, its
documentation, or other useful information related to developing `iesopt`. If you are only _using_ `iesopt` to develop
your own tools / projects, this will not be necessary to check at all.

If you are up- or downgrading `iesopt`, head over to the [Releases Page](https://github.com/ait-energy/iesopt/releases/)
that provides you with information on what changed between versions.

### Different projects

The following projects / repositories are part of _"IESopt"_:

- [`IESopt.jl`](https://github.com/ait-energy/IESopt.jl), the Julia-based core model powering all of IESopt's capabilities.
- [`iesopt`](https://github.com/ait-energy/iesopt), the Python interface (which you are currently viewing), which
enables a fast and simple application of `IESopt.jl`, without the need to know any Julia, or how to set it up. It further
provides different quality-of-life features, and embeds the model into a more conventional object-oriented style, that
you may be more used to - compared to the way Julia works.
- [`IESoptLib.jl`](https://github.com/ait-energy/IESoptLib.jl), the library of various assets related to IESopt. You can
find examples, as well as pre-defined templates and addons here. The library is automatically loaded for you.

## Installation

### Setting up an environment

:::{note}
Skip this step if you want to install `iesopt` into an existing environment and directly continue directly continue with
[Installing `iesopt`](#installing-iesopt).
:::

This assumes that you have a working `conda` executable installed on your system, e.g., after installing [Miniconda](https://docs.anaconda.com/miniconda/).
If you added the binary paths to your `PATH` environment variable, you should be able to execute the following steps in
every terminal (e.g., within [VSCode](https://code.visualstudio.com/)), otherwise make sure to use a proper shell - most
likely you _Anaconda Prompt_.

First we create a new environment using (make sure to replace `yourenvname` by a fitting name)

```bash
conda create -n yourenvname python=3.12 -y
conda activate yourenvname
```

Your terminal should now print the name of your environment in each new line, similar to

```bash
(yourenvname) user@PCNAME:~/your/current/path$
```

Next, we install [Poetry](https://python-poetry.org/) by executing

```bash
pip install poetry
```

and use it to create a new basic environment by executing

```bash
poetry init -n
```

Now you should see a new `pyproject.toml` file inside your folder, and are ready to [install `iesopt`](Installing `iesopt`).

:::{admonition} Learning more about managing dependencies with Poetry
:class: tip

Checkout the great tutorial ["Dependency Management With Python Poetry"](https://realpython.com/dependency-management-python-poetry/)
to learn more about all of this, or consult the [Basic usage](https://python-poetry.org/docs/basic-usage/) section of
the Poetry documentation.
:::

### Installing `iesopt`

This assumes that you have a working environment, that has Poetry installed. It should however work similarly using
`conda install` or `pip install` instead.

You can install `iesopt` by executing

```bash
poetry add iesopt
```

And that's it... you are done!

#### Precompiling

Julia, compared to Python as you are probably used to it, _compiles_ code [^compiling] just before it executes it. This,
coupled with the fact that we - until now - did not fully initialize our Julia environment, may lead to your first time
using `iesopt` taking a long (!) time.

To "prevent" this, we can do a lot of the heavy lifting right here and now, by starting Python. You can do this by just
executing `python` in the terminal that you used to set up everything, like so

```bash
(yourenvname) user@PCNAME:~/your/current/path$ python
```

which should result in an info message similar to this one:

```text
Python 3.11.9 (main, Apr 19 2024, 16:48:06) [GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Then just run

```python
import iesopt
```

You will see some messages like `INFO:iesopt:Setting up Julia ...`, and most likely a lot of other output related to the
instantiation of a Julia environment. This may take a few minutes, but should end with lines that print

```text
INFO:iesopt:Julia setup successful
INFO:iesopt:Importing Julia module `IESoptLib`
INFO:iesopt:Importing Julia module `IESopt`
INFO:iesopt:Importing Julia module `JuMP`
```

and are followed by a welcome message that documents the current version of IESopt that you are using. After that, you
are ready to start using `iesopt`.

:::{admonition} Reducing overhead
:class: hint

The next time that you launch `iesopt` by using `import iesopt` inside your current environment will be considerably
faster. Nonetheless, every new launch comes with certain compilation-related overheads. The best way to prevent this, is
making use of an interactive / REPL-based style of development.
:::

<!--- TODO: link to REPL explanation here --->

## Citing IESopt

If you find IESopt useful in your work, and are intend to publish or document your modeling, we kindly request that you
include the following citation:

- **Style: APA7**
  > Strömer, S., Schwabeneder, D., & contributors. (2021-2024). _IESopt: Integrated Energy System Optimization_ [Software]. AIT Austrian Institute of Technology GmbH. [https://github.com/ait-energy/IESopt](https://github.com/ait-energy/iesopt)
- **Style: IEEE**
  > [1] S. Strömer, D. Schwabeneder, and contributors, _"IESopt: Integrated Energy System Optimization,"_ AIT Austrian Institute of Technology GmbH, 2021-2024. [Online]. Available: [https://github.com/ait-energy/IESopt](https://github.com/ait-energy/iesopt)
- **BibTeX:**
  ```bibtex
  @misc{iesopt,
      author = {Strömer, Stefan and Schwabeneder, Daniel and contributors},
      title = {{IES}opt: Integrated Energy System Optimization},
      organization = {AIT Austrian Institute of Technology GmbH},
      url = {https://github.com/ait-energy/iesopt},
      type = {Software},
      year = {2021-2024},
  }
  ```

[^diataxis]: The structure of the documentation follows the [Diátaxis Framework](https://diataxis.fr), especially
related to [The difference between a tutorial and how-to guide](https://diataxis.fr/tutorials-how-to).
[^compiling]: If you are unsure what "compiling" actually means, you possibly could benefit from checking [differences between Julia and other languages](https://docs.julialang.org/en/v1/manual/noteworthy-differences/) (if you already know another programming language), or looking at [this discourse post](https://discourse.julialang.org/t/so-does-julia-compile-or-interpret/56073/2),
or even read more about [compilers](https://en.wikipedia.org/wiki/Compiler).
