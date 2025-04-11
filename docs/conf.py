import sys
from pathlib import Path
import importlib.metadata

from sphinxawesome_theme.postprocess import Icons


# -- Setup -------------------------------------------------------------------

DOCS = Path(__file__).parent
sys.path.insert(0, str((DOCS / "_extensions").resolve()))
sys.path.insert(0, str((DOCS / ".." / "src").resolve()))
sys.path.insert(0, str((DOCS / "..").resolve()))

CREATE_DYNAMIC_DOCSTRINGS = [
    # ("test", "getfield", "some_foo(...)")
    # and then use:
    # ```{include} ../../../dynamic/out/test.md
    # ```
]
if len(CREATE_DYNAMIC_DOCSTRINGS) > 0:
    import docs.dynamic.create as ddcreate

    ddcreate.create_md(CREATE_DYNAMIC_DOCSTRINGS)

import docs.dynamic.core as ddcore  # noqa: E402

ddcore._dyn_core_create_md("Connection")
ddcore._dyn_core_create_md("Decision")
ddcore._dyn_core_create_md("Node")
ddcore._dyn_core_create_md("Profile")
ddcore._dyn_core_create_md("Unit")

import docs.dynamic.julia  # noqa: E402, F401

# -- General -----------------------------------------------------------------

project = "IESopt"
copyright = "AIT Austrian Institute of Technology GmbH"
author = "S. Strömer (@sstroemer), D. Schwabeneder (@daschw)"
version = str(importlib.metadata.version("iesopt"))
release = version

extensions = [
    # "myst_parser",
    "myst_nb",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.githubpages",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.napoleon",
    "sphinx_togglebutton",
    "julia_domain",
    "sphinx.ext.mathjax",
]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]
source_suffix = {
    ".rst": "restructuredtext",
    ".ipynb": "myst-nb",
    ".myst": "myst-nb",
}
nb_custom_formats = {
    ".md": ["jupytext.reads", {"fmt": "myst"}],
}

intersphinx_mapping = {
    "IESopt": ("https://ait-energy.github.io/IESopt.jl/dev", None),
    "python": ("https://docs.python.org/3", None),
    "pandas": ("http://pandas.pydata.org/pandas-docs/dev", None),
}
intersphinx_disabled_reftypes = [""]

nb_execution_mode = "off"

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinxawesome_theme"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

html_permalinks_icon = Icons.permalinks_icon

pygments_style = "default"
pygments_style_dark = "lightbulb"

html_theme_options = {
    "show_breadcrumbs": True,
    "show_scrolltop": True,
    "awesome_external_links": True,
    "awesome_headerlinks": True,
    "show_prev_next": False,
    "main_nav_links": {
        "Home": "index",
        "GitHub": "https://github.com/ait-energy/iesopt",
        "IESopt.jl": "https://github.com/ait-energy/IESopt.jl",
    },
}

html_context = {
    "default_mode": "light",
}

html_favicon = "_static/favicon.ico"

# -- MyST & autodoc configuration --------------------------------------------

myst_enable_extensions = ["dollarmath", "amsmath", "colon_fence", "fieldlist"]
myst_heading_anchors = 3
autodoc_packages = ["../src/iesopt"]
suppress_warnings = ["autosectionlabel.*"]
autosection_label_prefix_document = True
