
import os
from setuptools import setup, find_namespace_packages

version="0.1.0"

if "BUILD_NUM" in os.environ.keys():
    version = version + "." + os.environ["BUILD_NUM"]

setup(
  name = "pytypeworks",
  packages=find_namespace_packages(where='src'),
  package_dir = {'' : 'src'},
  version=version,
  author = "Matthew Ballance",
  author_email = "matt.ballance@gmail.com",
  description = ("PyTypeWorks provides utilities for decorator-driven type manipulation and introspection."),
  long_description = """
  Python library for manipulating and introspecting types with decorators
  """,
  license = "Apache 2.0",
  keywords = ["Python", "Decorators"],
  url = "https://github.com/fvutils/pytypeworks",
  entry_points={ },
  setup_requires=[
    'setuptools_scm',
  ],
  install_requires=[ ],
)

