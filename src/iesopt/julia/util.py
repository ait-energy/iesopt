from ..util import logger, get_iesopt_module_attr, set_iesopt_module_attr


def jl_safe_seval(code: str):
    """Safely evaluate Julia code."""
    try:
        return get_iesopt_module_attr("julia").seval(code)
    except Exception as e:
        logger.error("Exception while trying to execute Julia code: `%s`" % code)
        raise e


def jl_import(module: str):
    """Import a Julia module."""
    logger.info("Importing Julia module `%s`" % module)
    jl_safe_seval(f"import {module}")


def jl_symbol(string: str):
    """Create a Julia `Symbol` from `string`.

    This function can be called as: :py:func:`iesopt.Symbol`, or :py:func:`iesopt.jl_symbol`.

    Arguments:
        string (str): The string to convert to a Julia `Symbol`.

    Returns:
        The Julia `Symbol` object.

    Examples:
        ..  code-block:: python
            :caption: Convert a string to a Julia `Symbol`

            import iesopt
            iesopt.jl_symbol(":iesopt")     # => `Julia: :iesopt`

        ..  code-block:: python
            :caption: Directly import and use the `Symbol` alias

            from iesopt import Symbol
            Symbol(":iesopt")               # => `Julia: :iesopt`

    """
    return get_iesopt_module_attr("julia").Symbol(string)


set_iesopt_module_attr("Symbol", jl_symbol)
