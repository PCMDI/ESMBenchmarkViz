from setuptools import find_packages, setup

# Read version from _version.py
version = {}
with open("ESMBenchmarkViz/_version.py") as f:
    exec(f.read(), version)

with open("README.md") as fr:
    long_description = fr.read()

setup(
    name="ESMBenchmarkViz",  # Replace with your package name
    version=version["__version__"],  # Initial version
    packages=find_packages(),  # Automatically find sub-packages
    install_requires=[  # Optional: add dependencies here
        # 'numpy>=1.18.0',
        # 'pandas>=1.0.0'
    ],
    author="Jiwoo Lee",
    author_email="lee1043@llnl.gov",
    description="A Python package for interactive visualizations for Earth System Model evaluation and benchmarking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lee1043/ESMBenchmarkViz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
