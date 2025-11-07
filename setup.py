"""Setup script for Voynich Morphemic Decryption."""

from pathlib import Path
from setuptools import setup, find_packages

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file, "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Read version
version_file = Path(__file__).parent / "VERSION"
version = version_file.read_text(encoding="utf-8").strip() if version_file.exists() else "1.0.0"

setup(
    name="voynich-morphemic-decryption",
    version=version,
    description="Advanced morphemic analysis & decryption of Voynich Manuscript",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mateusz Piesiak",
    author_email="mateuszpiesiak1990@gmail.com",
    url="https://github.com/mati83moni/voynich-morphemic-decryption",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.11.0",
            "ruff>=0.1.0",
            "mypy>=1.6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "voynich=voynich_decryption.cli.main:app",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    keywords="voynich manuscript morphemic-analysis nlp cryptography linguistics",
    project_urls={
        "Bug Reports": "https://github.com/mati83moni/voynich-morphemic-decryption/issues",
        "Source": "https://github.com/mati83moni/voynich-morphemic-decryption",
    },
)
