import pandas as pd
from ..util import logger, get_iesopt_module_attr


def jl_safe_seval(code: str):
    """Safely evaluate Julia code."""
    try:
        return get_iesopt_module_attr("julia").seval(code)
    except Exception as e:
        logger.error("Exception while trying to execute Julia code: `%s`" % code)
        logger.error("Exception: `%s`" % str(e))
        logger.error("Exception details: `%s`" % getattr(e, "exception", "missing"))

    return None


def jl_import(module: str):
    """Import a Julia module."""
    logger.info("    %s" % module)
    jl_safe_seval(f"import {module}")


def jl_symbol(string: str):
    """Create a Julia `Symbol` from `string`.

    This function should be called as `iesopt.Symbol`, but can also be called as `iesopt.jl_symbol`.

    Arguments:
        string (str): The string to convert to a Julia `Symbol`.

    Returns:
        The Julia `Symbol` object.

    Examples:
        ..  code-block:: python
            :caption: Directly import and use the `Symbol` alias

            from iesopt import Symbol
            Symbol(":iesopt")               # => `Julia: :iesopt`

    """
    return get_iesopt_module_attr("julia").Symbol(string)


def jl_isa(obj, julia_type: str):
    julia = get_iesopt_module_attr("julia")

    if julia_type == "AbstractVector":
        return julia.isa(obj, julia.AbstractVector)

    if julia_type == "AbstractSet":
        return julia.isa(obj, julia.AbstractSet)

    if julia_type == "AbstractDict":
        return julia.isa(obj, julia.AbstractDict)

    return julia.seval(f"(x) -> (x isa {julia_type})")(obj)


def jl_docs(obj: str, module: str = "IESopt"):
    """Get the documentation string of a Julia object inside the IESopt module."""
    julia_docstr = jl_safe_seval(f"@doc {module}.{obj}")
    if julia_docstr is None:
        return "Missing documentation string."
    try:
        return "".join(str(el) for el in julia_docstr.content)
    except Exception:
        return "".join(str(el) for el in julia_docstr.text)


def recursive_convert_py2jl(item):
    if isinstance(item, dict):
        julia = get_iesopt_module_attr("julia")
        convert = get_iesopt_module_attr("juliacall").convert
        return convert(julia.seval("Dict{String, Any}"), {k: recursive_convert_py2jl(v) for (k, v) in item.items()})
    elif isinstance(item, list):
        julia = get_iesopt_module_attr("julia")
        convert = get_iesopt_module_attr("juliacall").convert
        return convert(julia.seval("Vector{Any}"), [recursive_convert_py2jl(v) for v in item])
    elif isinstance(item, pd.DataFrame):
        julia = get_iesopt_module_attr("julia")
        return julia.IESopt.DataFrames.DataFrame(item)

    return item
