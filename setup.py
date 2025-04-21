from setuptools import setup, find_packages

setup(
    name="FuturePulse",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "plotly>=5.10.0",
        "pytest>=7.0.0",
    ],
    author="Lunapapa",
    author_email="info@lunapapa.eu",
    description="A library for backtesting price action trading strategies on ES futures",
    license="MIT",
    url="https://github.com/lunapapa-finland/Lunapulse",
)