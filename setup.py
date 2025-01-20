from setuptools import setup, find_packages

setup(
    name="llm-4x-game",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pytest>=7.4.4",
        "pytest-cov>=4.1.0",
    ],
    python_requires=">=3.10",
)