"""
Setup configuration for random-data-visualization package.
"""

from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="random-data-visualization",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python package for generating and visualizing random data with Matplotlib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/random-data-visualization",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Jupyter",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
    },
    keywords=[
        "visualization",
        "matplotlib",
        "data-science",
        "jupyter",
        "random-data",
        "plotting",
    ],
    project_urls={
        "Bug Reports": "https://github.com/yourusername/random-data-visualization/issues",
        "Source": "https://github.com/yourusername/random-data-visualization",
        "Documentation": "https://github.com/yourusername/random-data-visualization#readme",
    },
)