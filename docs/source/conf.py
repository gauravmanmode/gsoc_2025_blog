# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'GSoC 2025 Blog'

html_title = "GSoC 2025 Blog"  
copyright = '2025, gauravmanmode'
author = 'gauravmanmode'

# -- General configuration ---------------------------------------------------
extensions = [
    "myst_parser",          # Markdown support
    "sphinx.ext.mathjax",   # LaTeX math
    "sphinx.ext.githubpages",
]

myst_enable_extensions = [
    "dollarmath",   # $math$
    "amsmath",
    "colon_fence",
]

master_doc = 'report'

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'shibuya'

html_static_path = ["_static"]

html_css_files = [
    "a.css",
]
html_theme_options = {
    "page_layout": "default",
}

# extensions = [
#     "myst_nb",
# ]

# # optional: control execution
# nb_execution_mode = "auto"   # or "force" to always re-run, "off" to never
