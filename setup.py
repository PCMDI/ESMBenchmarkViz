from setuptools import find_packages, setup

setup(
    name="ESMBenchmarkViz",  # Replace with your package name
    version="0.1.0",  # Initial version
    packages=find_packages(),  # Automatically find sub-packages
    install_requires=[  # Optional: add dependencies here
        # 'numpy>=1.18.0',
        # 'pandas>=1.0.0'
    ],
    author="Jiwoo Lee",
    author_email="lee1043@llnl.gov",
    description="A Python package for interactive visualizations for Earth System Model evaluation and benchmarking",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lee1043/ESMBenchmarkViz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
