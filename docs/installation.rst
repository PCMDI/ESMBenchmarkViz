.. _installation:

Installation
============

The **ESMBenchmarkViz** package is not yet available on the conda-forge channel. To install it, you will need to clone the repository and install it locally using `pip`. The following steps will guide you through the process.

Prerequisites
-------------

- Python 3.10 or higher
- `git` installed on your system
- (Optional) `conda` for environment management

Step 1: Clone the Repository
----------------------------

Clone the repository from GitHub:

.. code-block:: bash

    git clone https://github.com/PCMDI/ESMBenchmarkViz.git
    cd ESMBenchmarkViz

Step 2: (Optional) Create and Activate a Conda Environment
----------------------------------------------------------

It is recommended to use a conda environment to manage dependencies. You can create and activate a new environment as follows:

.. code-block:: bash

    conda create -n esmbenchmarkviz python=3.9
    conda activate esmbenchmarkviz

Step 3: Install the Package
---------------------------

Install the package using `pip` from the root directory of the cloned repository:

.. code-block:: bash

    pip install .

Verifying the Installation
--------------------------

After installation, you can verify that the package is installed by running:

.. code-block:: bash

    python -c "import ESMBenchmarkViz; print(ESMBenchmarkViz.__version__)"

If you see the version number printed without errors, the installation was successful.

Troubleshooting
---------------

If you encounter any issues during installation, please check that you have the required dependencies and that you are using a compatible Python version. For further assistance, refer to the `README.md` in the repository or open an issue on the `ESMBenchmarkViz` GitHub page.

----

For more information, visit the project repository: https://github.com/PCMDI/ESMBenchmarkViz