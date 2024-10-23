"""Sphinx configuration"""
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

project = 'HaasLib'
copyright = '2024, Your Name'
author = 'Your Name'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_rtd_theme',
]

html_theme = 'sphinx_rtd_theme'
