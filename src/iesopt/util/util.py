import sys


def set_iesopt_module_attr(attr: str, value):
    """Set an internal attribute of the `iesopt` module."""
    sys.modules["iesopt"].__dict__[f"_!_attr_{attr}"] = value


def get_iesopt_module_attr(attr: str):
    """Get an internal attribute of the `iesopt` module."""
    return sys.modules["iesopt"].__dict__[f"_!_attr_{attr}"]
