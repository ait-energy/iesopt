# Integrated Energy System Optimization

<!--- TABLE OF CONTENTS STRUCTURE --->

:::{toctree}
:hidden:
:caption: IESopt
:maxdepth: 2

Introduction <self>
:::

:::{toctree}
:hidden:
:caption: Tutorials
:maxdepth: 2

getting_started.md
notebooks/first_model.ipynb
tocs/tutorials_extracting_results.md
tocs/tutorials_templates.md
pages/tutorials/addons.md

tocs/examples.md
:::

<!--- notebooks/mga_basic.ipynb --->

:::{toctree}
:hidden:
:caption: User guides

pages/user_guides/index.md
pages/user_guides/toc_general.md
pages/user_guides/toc_qna.md
:::

:::{toctree}
:hidden:
:caption: Manual

pages/manual/yaml/index.md
pages/manual/python/index.md
pages/manual/julia/index.md
:::

:::{toctree}
:hidden:
:caption: References

pages/references/publications.md
pages/references/projects.md
:::

:::{toctree}
:hidden:
:caption: Developer documentation

pages/dev/general.md
pages/dev/core.md
pages/dev/updating.md
:::

<!--- TABLE OF CONTENTS STRUCTURE --->

:::{admonition} _IESopt -- an Integrated Energy System Optimization framework._
:class: tip

Sound political and regulatory decisions require accurate studies and projections of the world's energy future to meet the rising challenges linked to climate change. 
IESopt, developed and maintained at the Center for Energy at AIT Austrian Institute of Technology GmbH, is an energy system modeling framework. 
It is fully implemented in Julia and making use of JuMP.jl to optimize energy systems that are characterized by a high degree of integration between different energy carriers and sectors. It focuses on offering a modular and adaptable tool for modelers, that does not compromise on performance, while still being user-friendly.

The modularity of the tool is given by the approach to not implement common energy system assets directly but specific abstract components instead, that can be configured and combined into, e.g., power plants, heat pumps, grid connections, or even complex multi-carrier storages. 
The user-friendliness is given by the requirement of only one single file being the mandatory input and by the utilization of commonly known keywords to parameterize the components in the YAML format. 
These two points enable users without detailed understanding of mathematical modeling or proficiency in any coding-language to use this tool. 

The framework provides numerous application possibilities: 
  - Household scheduling
  - Operational planning for industrial sites
  - Optimizing energy infrastructure such as hydrogen grids
  - Energy community design and analysis
  - Modelling future global energy systems
  - …
:::

:::{caution}
The documentation is currently being put together based on cleaned parts of the internal docs. Until this is finished, this documentation may contains some placeholders.
:::

## Overview

With a configuration YAML file you create a model of the desired system including all components, their parameters and corresponding input data like, e.g., generation profiles, to solve a problem or answer a question. 
Once you run the model it is by default optimized to minimize the total system costs, which is the objective value of the problem. 
For every component that you specified in the configuration you will get detailed results for each time step. Depending on the type of the component, there are different results available, for example an "expression_in" for the component type "Connection" which specifies the amount of energy going into the connection at this time step. The result labels are generated based on the problems' mathematical formulation, which is why there are expressions, variables, and constraints, as well as primal and dual results. 

For further description of the tools' functionalities also see the [^paper]. 

This overview of `iesopt`'s documentation [^diataxis] will help you know where to find what you are looking for.

### Using this documentation

To get started follow the instructions in {ref}`Getting started` to set up the environment and then create your first model by following the tutorial {ref}`a first model`. 
A quick overview how this documentation is structured to support you in learning IESopt and creating your own models: 

1. **Tutorials** will help you learn how to apply `iesopt`'s various main functionalities, to solve energy
system optimization models. Start with {ref}`examples` if you are new and have completed the {ref}`A first model` initial tutorial.
2. **User guides** provide various concise how-to guides, that help you accomplish a certain task, correctly
and safely. Consult these to remind yourself _how to do X_.
3. **Manual** contains technical reference for `IESopt.jl` core components, the YAML syntax, APIs, and more
internal details. It assumes that you already have a basic understanding of the core concepts of `iesopt`.
4. **References** lists publications and projects where IESopt was applied as part of the modeling approach. 
5. **Developer documentation** can be consulted for tips on how to improve `iesopt`, its
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
[^paper]: [IESopt: A Modular Framework for High-Performance Energy System Optimization](https://github.com/sstroemer/OSMSES2024/blob/main/paper_long_version.pdf)
[^diataxis]: The structure of the documentation follows the [Diátaxis Framework](https://diataxis.fr), especially
related to [The difference between a tutorial and how-to guide](https://diataxis.fr/tutorials-how-to).
[^compiling]: If you are unsure what "compiling" actually means, you possibly could benefit from checking [differences between Julia and other languages](https://docs.julialang.org/en/v1/manual/noteworthy-differences/) (if you already know another programming language), or looking at [this discourse post](https://discourse.julialang.org/t/so-does-julia-compile-or-interpret/56073/2),
or even read more about [compilers](https://en.wikipedia.org/wiki/Compiler).
