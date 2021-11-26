from setuptools import setup, find_packages

setup(
    name="dme",
    version="0.1.0",
    packages=find_packages(include=["dme", "dme.*"]),
    install_requires=[
        "requests",
    ],
    python_requires=">=3.7",
)
