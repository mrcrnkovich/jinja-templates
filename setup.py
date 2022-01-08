"""Script to setup a packaged version of the project"""

from setuptools import setup, find_packages

setup(
    name="jinja-templates",
    description="A templated report generator using jinja and yaml",
    version="1.0.0",
    author="mrc",
    packages=find_packages(),
)
