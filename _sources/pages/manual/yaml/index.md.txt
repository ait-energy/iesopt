# YAML

Most configuration settings for the IESopt optimization model are stored in YAML files. This section provides a reference for the YAML syntax and the specific settings used in IESopt.

## Yet another markup language?

YAML - which actually stands for _YAML Ain't Markup Language_ - is a human-readable data serialization language. It is often used for configuration files and data exchange between languages. YAML is a superset of JSON, meaning that any valid JSON file is also a valid YAML file.

You can find more information at:

- [The official YAML website](https://yaml.org/)
- [The `YAML.jl` Julia package](https://github.com/JuliaData/YAML.jl)
- Various good Python oriented sources, such as this [realpython tutorial](https://realpython.com/python-yaml/) or the [PyYAML package](https://github.com/yaml/pyyaml)

## Good to know

The following points offer hints, notes, or recommendations for working with YAML files in IESopt:

- **Indentation**: YAML files make use of indentation: The recommended indentation is two spaces.
- **Comments**: Comments in YAML files are preceded by a `#` character.
- **Dictionaries**: YAML files are often used to define dictionaries. In Python (and Julia), dictionaries are/were unordered[^order], and the order of (dictionary) entries are therefore not considered to have any specific order. However, the order given in the documentation is recommended for readability.

```{danger}
Since we are using dictionaries to store most configurations inside the YAML files, be aware that keys have to be unique. No key can exist twice in the same dictionary - this means, e.g., that you cannot use two components with the same name. However, depending on the implementation of the YAML parser, duplicate keys might not raise an error: After loading a YAML file IESopt will only be able to see the last value of a duplicate key, without any way to detect that ambiguity.

**This is a common source of errors, so be careful!**
```

## Contents

See the documentation of the built-in YAML here:

:::{toctree}
top_level.md
core_components.md
:::

[^order]: While `dict`s are standardized to be ordered starting with Python 3.7, and options like `OrderedCollections.jl` in Julia exist, the existence of these options is not guaranteed in all environments, and considering all potential parsers.
