import os
import sys
from pathlib import Path

from sphinxawesome_theme.postprocess import Icons


# -- Setup -------------------------------------------------------------------

DOCS = Path(__file__).parent
sys.path.insert(0, str((DOCS / "_extensions").resolve()))
sys.path.insert(0, str((DOCS / ".." / "src").resolve()))
sys.path.insert(0, str((DOCS / "..").resolve()))
os.environ["IESOPT_DOCS_NOEXEC"] = "true"

# -- General -----------------------------------------------------------------

project = "IESopt"
copyright = "AIT Austrian Institute of Technology GmbH"
author = "S. Strömer (@sstroemer), D. Schwabeneder (@daschw)"
version = "1.0.0"  # TODO: get from iesopt.__version__
release = version

extensions = [
    "myst_nb",
    #    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.githubpages",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.napoleon",
    "julia_domain",
    "sphinx.ext.mathjax",
]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]
source_suffix = {
    ".rst": "restructuredtext",
    ".ipynb": "myst-nb",
    ".myst": "myst-nb",
}

intersphinx_mapping = {"IESopt": ("https://ait-energy.github.io/IESopt.jl/dev", None)}
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
}

# -- MyST & autodoc configuration --------------------------------------------

myst_enable_extensions = ["dollarmath", "amsmath", "colon_fence"]
myst_heading_anchors = 3
autodoc_packages = ["../src/iesopt"]
