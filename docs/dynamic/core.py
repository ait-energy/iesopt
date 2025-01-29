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


# def _md_table_to_dict(md: str):
#     lines = md.strip().splitlines()
#     headers = [header.strip() for header in lines[0].split("|")[1:-1]]
#     data = []

#     for row in lines[2:]:  # skip header and divider lines
#         values = [value.strip() for value in row.split("|")[1:-1]]
#         data.append(dict(zip(headers, values)))

#     return data


# def _trf_overview(doc: str):
#     # doc = doc.replace('!!! details "Basic Examples"', ":::{admonition} \"Basic Examples\"\n:class: dropdown\n")
#     doc = doc.replace('!!! details "Basic Examples"', "## Basic Examples\n\n")
#     doc = re.sub(r"^ {0,4}", "", doc, flags=re.MULTILINE)
#     return doc + "\n"


# def _trf_parameters(doc: str):
#     ret = ""
#     data = _md_table_to_dict(doc)

#     for item in data:
#         ret += f"### {item.pop('Name').replace('`', '')}\n\n"
#         ret += f"{item.pop('Description')}\n\n"
#         for k, v in item.items():
#             ret += f":{k}: {v}\n"

#     return ret


# def _add_details(info: str):
#     ret = ""
#     for entry in info.split("!!! details ")[1:]:
#         entry = re.sub(r"^ {0,4}", "", entry, flags=re.MULTILINE)
#         entry = re.sub(r'!!! tip "([^"]+)"', r":::{admonition} \1\n    :class: dropdown", entry)
#         entry = entry.replace("!!! tip", ":::{tip}")
#         entry = re.sub(r'!!! info "([^"]+)"', r":::{admonition} \1\n    :class: dropdown", entry)
#         entry = entry.replace("!!! info", ":::{hint}")
#         # TODO: add other admonition conversions
#         lines = entry.splitlines()
#         title = lines[0].replace('"', "")
#         ret += f"\n\n#### {title}" + "\n\n"
#         is_in_adm = False
#         for line in lines[1:]:
#             if len(line) == 0:
#                 continue

#             if is_in_adm and line[0] != "\n" and line[0] != " ":
#                 is_in_adm = False
#                 ret += ":::\n\n"

#             if is_in_adm:
#                 ret += line[4:] + "\n"
#             else:
#                 ret += line + "\n"
#             if line.startswith(":::"):
#                 is_in_adm = True
#         if is_in_adm:
#             ret += ":::\n\n"
#     return ret


# def _trf_details(doc: str):
#     tmp = doc.strip().split("## Variables")[1]

#     tmp = tmp.split("## Expressions")
#     details_var = tmp[0].strip()

#     tmp = tmp[1].split("## Constraints")
#     details_exp = tmp[0].strip()

#     tmp = tmp[1].split("## Objectives")
#     details_con = tmp[0].strip()
#     details_obj = tmp[1].strip()

#     ret = "### Variables\n\n"
#     ret += _add_details(details_var)

#     ret += "### Expressions\n\n"
#     ret += _add_details(details_exp)

#     ret += "### Constraints\n\n"
#     ret += _add_details(details_con)

#     ret += "### Objectives\n\n"
#     ret += _add_details(details_obj)

#     return ret


def _getdd(cc: str):
    dt = iesopt.julia.seval(f"IESopt.{cc}")
    return iesopt.IESopt._get_dynamic_documentation(dt)


def _dyn_core_create_md(cc: str):
    docs = _getdd(cc)

    main_docstr = docs["docstr_main"]
    final_main_docstr = ""
    if '!!! details "Basic Examples"' in main_docstr:
        within_example = False
        for line in main_docstr.splitlines():
            if not within_example:
                if line == '!!! details "Basic Examples"':
                    final_main_docstr += ":::{admonition} **Basic Examples**\n:class: dropdown\n\n"
                    within_example = True
                else:
                    final_main_docstr += line + "\n"
            else:
                final_main_docstr += line[4:] + "\n"
        final_main_docstr = final_main_docstr + ":::"
    else:
        final_main_docstr = main_docstr

    with open(DYNAMIC / ".." / "pages" / "manual" / "yaml" / "core" / f"{cc.lower()}.md", "w") as f:
        f.write(f"# {cc}\n\n")
        f.write(DYN_CORE_HEADER_NOTE)
        f.write(f"{final_main_docstr}\n\n")

        f.write("## Parameters\n\n")
        for field in docs["fields_all"]:
            if field not in docs["docstr_fields"]:
                continue

            f.write(f"### `{field}`\n\n")
            f.write(f"{docs['docstr_fields'][field]['description']}\n\n")

            for p in ["mandatory", "default", "values", "unit"]:
                val = docs["docstr_fields"][field][p]
                if p == "default":
                    val = val.strip("`")
                    val = f"${val}$"
                f.write(f"- **{p}:** {val}\n")

            f.write("\n\n")

        f.write("## Detailed reference\n\n\n")

        for detail in ["Expressions", "Variables", "Constraints", "Objectives"]:
            f.write(f"### {detail}\n\n")

            funcs = docs["functions"][detail[0:3].lower()]
            for func in funcs:
                info = docs["docstr_functions"][func]
                f.write(f"#### `{info['name']}`\n\n")

                f.write(
                    f":::{{admonition}} How to access this {info['type_long']}?\n:class: dropdown\n\n"
                    f"```julia\n"
                    f"# Using Julia (`IESopt.jl`):\n"
                    f"import IESopt\n\n"
                    f"model = IESopt.run(...)  # assuming this is your model\n"
                    f'IESopt.get_component(model, "your_{info["component"]}").{info["type_short"]}.{info["name"]}\n'
                    f"```\n\n"
                    f"```python\n"
                    f"# Using Python (`iesopt`):\n"
                    f"import iesopt\n\n"
                    f"model = iesopt.run(...)  # assuming this is your model\n"
                    f'model.get_component("your_{info["component"]}").{info["type_short"]}.{info["name"]}\n'
                    f"```\n\n"
                    f":::\n\n"
                )

                f.write(
                    f"Full implementation and all details: [`{info['component']}/{info['type_short']}_{info['name']} @ IESopt.jl`](https://github.com/{info['code_path']})\n\n"
                )
                ds = info["docstr"]
                is_in_math_mode = False
                is_in_admonition = False
                for line in ds.splitlines():
                    if len(line) == 0:
                        if is_in_math_mode:
                            f.write("\n")
                        elif not is_in_admonition:
                            # This is necessary to create a new line in markdown, because Sphinx swallows these ...
                            f.write("> \n> &nbsp;\n> \n")
                        continue

                    line = line.lstrip(">")

                    if line.lstrip("> ").startswith("$$"):
                        # Math mode from Julia Markdown.
                        if is_in_math_mode:
                            f.write("$$\n")
                        else:
                            f.write("$$\n")
                        is_in_math_mode = not is_in_math_mode
                        continue
                    elif line.startswith("!!!"):
                        # Admonition from Julia Markdown.
                        assert not is_in_admonition  # currently can't handle nested admonitions
                        is_in_admonition = not is_in_admonition
                        res = line.split(maxsplit=2)
                        if len(res) == 2:
                            f.write(f":::{{{res[1]}}}\n\n")
                        elif len(res) == 3:
                            _stripped = res[2].strip('"')
                            f.write(f":::{{admonition}} **{_stripped}**\n:class: {res[1]}\n\n")
                        continue

                    if is_in_math_mode:
                        f.write(f"{line.lstrip('> ')}\n")
                    elif is_in_admonition:
                        if line.startswith("    "):
                            f.write(f"{line.lstrip()}\n")
                        else:
                            f.write(":::\n")
                            f.write(f"> {line.lstrip()}\n")
                            is_in_admonition = not is_in_admonition
                    else:
                        f.write(f"> {line.lstrip()}\n")

                if is_in_admonition:
                    f.write(":::\n")
                # ds = str(info["docstr"]).replace("\n", "\n> ")  ## TODO: remove str
                # f.write(f"> {ds}\n\n")
