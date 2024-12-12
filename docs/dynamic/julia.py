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
            if str(name) in ["IESU"]:
                # Just an abbreviation.
                continue

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
            if str(name) in ["Connection", "Decision", "Node", "Profile", "Unit"]:
                continue
            entries["types"].append((str(name), obj))
        else:
            print("ERROR - Unknown object type:", name, iesopt.julia.typeof(obj))

    return entries


entries = doc_julia_module(iesopt.IESopt)


def split_docstr(ds: str):
    if ds[1] != " ":
        return ("", ds)

    head = ""
    content = ""

    in_head = True
    for line in ds.split("\n"):
        if (not line.startswith("    ")) and (len(line) > 1):
            in_head = False
        if in_head:
            head += line[4:] + "\n"
        else:
            content += line + "\n"

    return (head, content)


def escape_md(md: str):
    ret = ""
    within_code = False
    for line in md.splitlines(True):
        if line.startswith("```"):
            within_code = not within_code

        if within_code:
            ret += line
            continue
        else:
            line = line.strip(" ")

        if line.startswith("#"):
            line = line.strip("#")
            line = line.strip(" \n")
            line = f"_**{line}**_  \n"

        ret += line

    return ret


with open(DYNAMIC / ".." / "pages" / "manual" / "julia" / "index.md", "w") as f:
    with open(DYNAMIC / ".." / "pages" / "manual" / "julia" / "index.md_template", "r") as ft:
        f.write(ft.read())

    for header in ["Types", "Macros", "Functions"]:
        f.write(f"### {header}\n\n")
        for item in entries[header.lower()]:
            if item[0].startswith("_"):
                # Skip "private" stuff that may "exported" for internal reasons.
                continue
            f.write(f"#### `{item[0]}`\n\n")

            docstr = split_docstr(iesopt.jl_docs(item[0], "IESopt"))
            if docstr[0] != "":
                f.write(f"```julia\n{docstr[0]}\n```\n\n")
            if docstr[1] != "":
                f.write(f"{escape_md(docstr[1])}\n\n")

            f.write("---\n\n")


for module in entries["modules"]:
    with open(DYNAMIC / ".." / "pages" / "manual" / "julia" / f"{module.lower()}.md", "w") as f:
        f.write(f"# {module}\n\n")
        f.write(DYN_CORE_HEADER_NOTE)

        f.write(split_docstr(iesopt.jl_docs(module))[1])
        f.write("\n\n")

        f.write("## API Reference\n\n")

        for header in ["Types", "Macros", "Functions"]:
            f.write(f"### {header}\n\n")
            for item in entries["modules"][module][header.lower()]:
                if item[0].startswith("_"):
                    # Skip "private" stuff that may "exported" for internal reasons.
                    continue
                f.write(f"#### `{item[0]}`\n\n")

                docstr = split_docstr(iesopt.jl_docs(item[0], f"IESopt.{module}"))
                if docstr[0] != "":
                    f.write(f"```julia\n{docstr[0]}\n```\n\n")
                if docstr[1] != "":
                    f.write(f"{escape_md(docstr[1])}\n\n")

                f.write("---\n\n")
