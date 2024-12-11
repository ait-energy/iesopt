import iesopt
from pathlib import Path


# Make sure we are using the latest version.
# This is necessary to pull in changes that may be present when an `.env` file with
# ```
# IESOPT_CORE = "https://github.com/username/IESopt.jl#feature-branch-name"
# ```
# is present in the root of the repository.
# This takes a bit of time even if nothing changes, but it's rather quick in that case.
iesopt.julia.seval('import Pkg; Pkg.update("IESopt")')


DYNAMIC = Path(__file__).parent

DYN_CORE_HEADER_NOTE = """```{note}
This section of the documentation is auto-generated from the code of the Julia-based core model. Refer to [IESopt.jl](https://github.com/ait-energy/IESopt.jl) for any further details (which may require some familiarity with Julia).

**If you spot incorrect math-mode rendering**, or similar issues, please [file an issue](https://github.com/ait-energy/iesopt/issues), since rendering documentation from Julia to Python is not the easiest task.
```

## Overview

"""


def doc_julia_module(module):
    entries = {"functions": [], "macros": [], "types": [], "modules": {}}

    for name in iesopt.julia.names(module):
        obj = iesopt.julia.getfield(module, name)

        if obj == module:
            continue

        if iesopt.jl_isa(obj, "Module"):
            # Create a subpage for this.
            entries["modules"][str(name)] = doc_julia_module(obj)
            # TODO: this does not work since stuff is not exported internally...
        elif iesopt.jl_isa(obj, "Function"):
            if str(name).startswith("@"):
                entries["macros"].append((str(name), obj))
            else:
                entries["functions"].append((str(name), obj))
        elif iesopt.jl_isa(obj, "Type"):
            # A struct, check if we should exclude it.
            if name in ["Connection", "Decision", "Node", "Profile", "Unit"]:
                continue
            entries["types"].append((str(name), obj))
        else:
            print("ERROR - Unknown object type:", name, iesopt.julia.typeof(obj))

    return entries


entries = doc_julia_module(iesopt.IESopt)

for entry in entries["modules"]:
    with open(DYNAMIC / ".." / "pages" / "manual" / "julia" / f"{entry.lower()}.md", "w") as f:
        f.write(f"# {entry}\n\n")
        f.write(DYN_CORE_HEADER_NOTE)
        f.write("docstr here...\n\n")

        f.write("## API Reference\n\n")

        for header in ["Types", "Macros", "Functions"]:
            f.write(f"### {header}\n\n")
            for item in entries[header.lower()]:
                f.write(f"#### {item[0]}\n\n")
                f.write(f"```julia\n{iesopt.jl_docs(item[1])}\n```\n\n")
                f.write("---\n\n")
