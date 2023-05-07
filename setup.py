import setuptools

from marshy.__version__ import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="marshy",
    version=__version__,
    author="Tim O'Farrell",
    author_email="tofarr@gmail.com",
    description="A convention over configuration approach to object marshalling.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tofarr/marshy",
    packages=setuptools.find_packages(include=["marshy*"]),
    install_requires=["typing-inspect~=0.7", "black"],
    setup_requires=[
        "black~=23.3",
        "marshmallow-dataclass~=8.5",
        "pytest~=7.2",
        "pytest-cov~=4.0",
        "pytest-xdist~=3.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
