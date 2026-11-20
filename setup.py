from setuptools import setup, find_packages

setup(
    name="QSERemediation",
    version="1.0.a",
    packages=find_packages(),
    install_requires=[
        "flask>=2.3.0",
        "sqlalchemy>=2.0.0",
        "pycryptodome>=3.19.0",
        "cryptography>=44.0.0",
        "pyjwt>=2.8.0",
        "requests>=2.31.0",
        "liboqs-python>=0.10.0",
    ],
)
