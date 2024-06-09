import sys
import importlib.metadata

# Set version.
__version__ = importlib.metadata.version("iesopt")

# Setup Julia.
from iesopt.julia import JULIA_STATE as __JULIA_STATE, julia as __julia

# Export everything.
from iesopt.model import Model
from iesopt.results import Results
from iesopt.iesopt import run

# ==================================================================
# "Re-define" constants, to allow showing them in the documentation.

JULIA_STATE = __JULIA_STATE
"""The current state of the Julia setup."""

julia = __julia
"""
The Julia object, if setup was successful.

..  code-block:: python
    :caption: Usage

    import iesopt
    iesopt.julia.println("Hello, from Julia's world!")
"""
