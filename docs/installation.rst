.. _installation:

Installation
============

The **ESMBenchmarkViz** package is not yet available on the conda-forge channel. To install it, you will need to clone the repository and install it locally using `pip`. The following steps will guide you through the process.

Prerequisites
-------------

- Python 3.10 or higher
- `git <https://github.com/git-guides/install-git>`_ and `pip <https://pip.pypa.io/en/stable/installation/>`_ installed on your system
- `numpy <https://numpy.org/>`_, `bokeh <https://docs.bokeh.org/en/latest/>`_, `matplotlib <https://matplotlib.org/>`_ libraries installed (These will be installed automatically if you follow the conda environment setup in Step 2)
- (Optional, but recommended) `conda <https://docs.conda.io/en/latest/>`_ for environment management

Step 1: Clone the Repository
----------------------------

Clone the repository from `GitHub <https://github.com/PCMDI/ESMBenchmarkViz.git>`_ to your local machine:

.. code-block:: bash

    git clone https://github.com/PCMDI/ESMBenchmarkViz.git
    cd ESMBenchmarkViz

Step 2: (Optional) Create and Activate a Conda Environment
----------------------------------------------------------

It is recommended to use a `conda <https://docs.conda.io/en/latest/>`_ environment to manage dependencies. You can create and activate a new environment as follows:

.. code-block:: bash

    conda create -n esmbenchmarkviz -f conda_env/environment.yml
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

If you encounter any issues during installation, please check that you have the required dependencies and that you are using a compatible Python version. For further assistance, refer to the `README.md <https://github.com/PCMDI/ESMBenchmarkViz/blob/main/README.md>`_ in the repository or open an issue on the `ESMBenchmarkViz GitHub page <https://github.com/PCMDI/ESMBenchmarkViz/issues>`_.

----

For more information, visit the project repository: https://github.com/PCMDI/ESMBenchmarkViz