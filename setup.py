import setuptools
from setuptools import find_namespace_packages

# with open("README.md", encoding="utf8") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="pysb-pkpd",
    version="0.2.1",
    python_requires=">=3.8",
    install_requires=["pysb>=1.15.0"],
    extras_require={"cython": "cython>=0.29.25"},
    author="Blake A. Wilson",
    author_email="blakeaw1102@gmail.com",
    description="PySB add-on providing domain-specific macros and models for pharmacological PK/PD modeling.",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/blakeaw/pysb-pkpd",
    packages=find_namespace_packages(where='src'),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)