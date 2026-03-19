.. ESMBenchmarkViz documentation master file


***************
ESMBenchmarkViz
***************

The `ESMBenchmarkViz` package provides tools for interactive visualization of results from the Earth System Model (ESM) Benchmarking project.

ESMs integrate key components of the climate system, including the atmosphere, oceans, land surface, and biosphere. They are used to study Earth system processes, feedbacks, and responses to external forcing. As ESMs increase in complexity, clear and reliable evaluation and benchmarking becomes increasingly important.

Model evaluation typically compares ESM output to observational datasets and to other models. These comparisons help quantify performance, identify strengths and weaknesses, guide model development, and improve confidence in scientific conclusions.

`ESMBenchmarkViz` offers reusable, high level plotting functions designed for ESM evaluation, intercomparison, and benchmarking. The package focuses on three core interactive visualizations:

(a) Taylor Diagram  
(b) Portrait Plot  
(c) Scatter plot with optional side “dive down” image viewer

For interactive plots, users can hover over points to view detailed tooltips, and, when enabled, click a point to open the associated “dive down” diagnostic image for deeper inspection.

The toolkit is developed in Python 3 and built on top of the `bokeh` library. API reference documentation and interactive demo Jupyter notebooks are provided for each plot type. The simple, function based API supports integration into existing analysis workflows and promotes reproducible climate research. Typical interactions include zooming, filtering, and tooltips, with optional side panel display for additional details.

Development of `ESMBenchmarkViz` originated from the interactive visualization dashboard of the `Program for Climate Model Diagnosis and Intercomparison (PCMDI) Metrics Package <https://pcmdi.github.io/pcmdi_metrics/>`_. This dashboard presents model evaluation metrics along with related diagnostic outputs (`https://pcmdi.llnl.gov/research/metrics/`). We refer to these diagnostics as “dive down information” because they help users investigate individual metrics in greater detail.


Getting Started
===============

* `Installation`_
* `Gallery`_

.. _Installation: installation
.. _Gallery: gallery


References
==========

Lee, J., K. Y. Chang, P. Gleckler, P. Ullrich, 2026: ESMBenchmarkViz: A Python Toolkit for Interactive Visualization of Earth System Model Evaluation and Benchmarking. Journal of Open Source Software (under review)

Acknowledgement
===============

Huge thank you to all of the ESMBenchmarkViz contributors!

ESMBenchmarkViz is developed by scientists and developers from the Program for Climate Model Diagnosis and
Intercomparison (`PCMDI`_) at Lawrence Livermore National Laboratory (`LLNL`_). 
This work is sponsored by the Regional and Global Model Analysis (`RGMA`_) program of 
the Earth and Environmental Systems Sciences Division (`EESSD`_) in 
the Office of Biological and Environmental Research (`BER`_) 
within the `Department of Energy`_'s `Office of Science`_. 
The work is performed under the auspices of the U.S. Department of Energy by 
Lawrence Livermore National Laboratory under Contract DE-AC52-07NA27344.

.. _LLNL: https://www.llnl.gov/
.. _PCMDI: https://pcmdi.llnl.gov/
.. _RGMA: https://climatemodeling.science.energy.gov/program/regional-global-model-analysis
.. _EESSD: https://science.osti.gov/ber/Research/eessd
.. _BER: https://science.osti.gov/ber
.. _Department of Energy: https://www.energy.gov/
.. _Office of Science: https://science.osti.gov/
.. _obs4MIPs: https://pcmdi.github.io/obs4MIPs/


License
=======

BSD 3-Clause License.

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: For users:

   overview
   installation
   gallery

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Reference:

   api

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Links:

   Source code <https://github.com/lee1043/ESMBenchmarkViz>
   Issue tracker <https://github.com/lee1043/ESMBenchmarkViz/issues>
