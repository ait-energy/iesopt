import iesopt
import re
from pathlib import Path


DYNAMIC = Path(__file__).parent

DYN_CORE_HEADER_NOTE = """```{caution}
Proper transformation (from Julia docs to Python docs) of math mode rendering, and therefore the "detailed model reference", is partially broken. Until this is fixed, please refer to the original Julia documentation for any math mode rendering.
```

## Overview

```{note}
This section of the documentation is auto-generated from the code of the Julia-based core model. Refer to [IESopt.jl](https://github.com/ait-energy/IESopt.jl) and its documentation for any further details (which may require some familiarity with Julia).
```

"""


def _md_table_to_dict(md: str):
    lines = md.strip().splitlines()
    headers = [header.strip() for header in lines[0].split("|")[1:-1]]
    data = []

    for row in lines[2:]:  # skip header and divider lines
        values = [value.strip() for value in row.split("|")[1:-1]]
        data.append(dict(zip(headers, values)))

    return data


def _trf_overview(doc: str):
    # doc = doc.replace('!!! details "Basic Examples"', ":::{admonition} \"Basic Examples\"\n:class: dropdown\n")
    doc = doc.replace('!!! details "Basic Examples"', "## Basic Examples\n\n")
    doc = re.sub(r"^ {0,4}", "", doc, flags=re.MULTILINE)
    return doc + "\n"


def _trf_parameters(doc: str):
    ret = ""
    data = _md_table_to_dict(doc)

    for item in data:
        ret += f"### {item.pop('Name').replace('`', '')}\n\n"
        ret += f"{item.pop('Description')}\n\n"
        for k, v in item.items():
            ret += f":{k}: {v}\n"

    return ret


def _add_details(info: str):
    ret = ""
    for entry in info.split("!!! details ")[1:]:
        entry = re.sub(r"^ {0,4}", "", entry, flags=re.MULTILINE)
        entry = re.sub(r'!!! tip "([^"]+)"', r":::{admonition} \1\n    :class: dropdown", entry)
        entry = entry.replace("!!! tip", ":::{tip}")
        entry = re.sub(r'!!! info "([^"]+)"', r":::{admonition} \1\n    :class: dropdown", entry)
        entry = entry.replace("!!! info", ":::{hint}")
        # TODO: add other admonition conversions
        lines = entry.splitlines()
        title = lines[0].replace('"', "")
        ret += f"\n\n#### {title}" + "\n\n"
        is_in_adm = False
        for line in lines[1:]:
            if len(line) == 0:
                continue

            if is_in_adm and line[0] != "\n" and line[0] != " ":
                is_in_adm = False
                ret += ":::\n\n"

            if is_in_adm:
                ret += line[4:] + "\n"
            else:
                ret += line + "\n"
            if line.startswith(":::"):
                is_in_adm = True
        if is_in_adm:
            ret += ":::\n\n"
    return ret


def _trf_details(doc: str):
    tmp = doc.strip().split("## Variables")[1]

    tmp = tmp.split("## Expressions")
    details_var = tmp[0].strip()

    tmp = tmp[1].split("## Constraints")
    details_exp = tmp[0].strip()

    tmp = tmp[1].split("## Objectives")
    details_con = tmp[0].strip()
    details_obj = tmp[1].strip()

    ret = "### Variables\n\n"
    ret += _add_details(details_var)

    ret += "### Expressions\n\n"
    ret += _add_details(details_exp)

    ret += "### Constraints\n\n"
    ret += _add_details(details_con)

    ret += "### Objectives\n\n"
    ret += _add_details(details_obj)

    return ret


def _dyn_core_create_md(cc: str):
    docstr = iesopt.get_jl_docstr(cc)

    tmp = docstr.split("# Parameters")
    docstr_overview = _trf_overview(tmp[0])

    tmp = tmp[1].split("# Detailed Model Reference")
    docstr_parameter = _trf_parameters(tmp[0])
    docstr_details = _trf_details(tmp[1])

    with open(DYNAMIC / ".." / "pages" / "manual" / "yaml" / "core" / f"{cc.lower()}.md", "w") as f:
        f.write(f"# {cc}")
        f.write("\n\n")
        f.write(DYN_CORE_HEADER_NOTE)
        f.write(docstr_overview)
        f.write("\n\n")
        f.write("## Parameters")
        f.write("\n\n")
        f.write(docstr_parameter)
        f.write("\n\n")
        f.write("## Detailed model reference")
        f.write("\n\n")
        f.write(docstr_details)
