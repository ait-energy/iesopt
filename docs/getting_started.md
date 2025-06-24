# Installation
## Setting up an environment
:::{note} avoid unnecessary initialization
:class: hint
Skip this step if you've already cloned a repository or want to install `iesopt` into an existing environment and directly continue with
[Installing `iesopt`](#installing-iesopt).
:::

Prerequisites: uv (python package manager, to install head over to [installation](https://docs.astral.sh/uv/getting-started/installation/))

The IESopt Project Template simplifies the setup steps and creates a pre-defined project structure for IESopt projects. Head over to the [repository](https://github.com/ait-energy/iesopt-project-template) and follow the instructions described in the README. You can skip all following steps on the current page. 

In case you don't want to use the IESopt Project Template continue with the following steps: 

In the command prompt make sure you are already inside the project folder that you want to develop in and run:

```bash
uv init
```

This creates a basic python project setup for you, including a sample Python file that you can run.

You can make sure all dependencies are actually installed using

```bash
uv sync
```

which you can also use to install everything after you've cloned a repository (because then you obviously don't need the `uv init` step).

You can test if everything works as expected by running

```bash
uv run main.py
```

If everything works, you are ready to install `iesopt`!

### Installing `iesopt`

This assumes that you have a working environment, managed by `uv`. It should however work similarly using
`conda`, `pip`, or `poetry` instead.

You can install `iesopt` by executing

```bash
uv add iesopt
```

And that's it... you are done!

#### Precompiling

Julia, compared to Python as you are probably used to it, _compiles_ code [^compiling] just before it executes it. This,
coupled with the fact that we - until now - did not fully initialize our Julia environment, may lead to your first time
using `iesopt` taking a long (!) time.

To "prevent" this, we can do a lot of the heavy lifting right here and now, by starting Python. You can do this by just
executing `python` in the terminal that you used to set up everything, like so

```bash
(yourenvname) user@PCNAME:~/your/current/path$ uv run python
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

To learn more about "REPL-based" development consult [this introductory guide](https://code.visualstudio.com/docs/python/run) that contains a direct showcase of how this works in VSCode. If you are a fan of "notebooks" in general, consider using the "native REPL" mode, otherwise give the "terminal REPL" a try (which is also extremely similar to the way Julia development works).



