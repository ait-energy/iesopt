import os
import sys
from pathlib import Path


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

extensions = ["myst_parser", "sphinx.ext.autodoc", "sphinx.ext.intersphinx", "sphinx.ext.githubpages", "julia_domain", "sphinx.ext.napoleon"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
source_suffix = [".md", ".rst"]

intersphinx_mapping = {"IESopt": ("https://ait-energy.github.io/IESopt.jl/dev", None)}
intersphinx_disabled_reftypes = [""]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinxawesome_theme"
html_static_path = ["_static"]

from sphinxawesome_theme.postprocess import Icons
html_permalinks_icon = Icons.permalinks_icon

pygments_style = "default"
pygments_style_dark = "lightbulb"

html_theme_options = {
   "show_breadcrumbs": True,
   "show_scrolltop": True,
}

# -- MyST & autodoc configuration --------------------------------------------

myst_enable_extensions = ["dollarmath", "amsmath", "colon_fence"]
myst_heading_anchors = 3
autodoc_packages = ["../src/iesopt"]
