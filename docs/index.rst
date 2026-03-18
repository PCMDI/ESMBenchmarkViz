.. ESMBenchmarkViz documentation master file


***************
ESMBenchmarkViz
***************

The `ESMBenchmarkViz` package provides a set of tools to visualize data from the Earth System Model (ESM) Benchmarking project. 

ESMs are essential for understanding and predicting the complex interactions within the Earth's climate system. These models integrate components such as the atmosphere, oceans, land surface, and biosphere to address fundamental and applied questions about Earth system processes, feedbacks, and the system’s response to external forcing. As ESMs grow in complexity, the need for effective evaluation and benchmarking methods to ensure their reliability and accuracy becomes increasingly important.

Evaluating ESMs involves comparing model outputs against observational data and other models to assess performance. This process is vital for identifying model strengths and weaknesses, guiding improvements, and deepening our understanding of climate processes. 

`ESMBenchmarkViz` provides reusable functions to generate a suite of interactive plots customized for the evaluation, intercomparison, and benchmarking of ESMs. The toolkit is developed in Python 3 and built on top of the Bokeh library for interactive visualization. API reference documentation and interactive demo Jupyter notebooks are available for each type of plot.

With singular functions for each plot, the library integrates seamlessly with existing data analysis workflows and promotes reproducibility in climate research. Users can interact with data by zooming, filtering, and hovering for detailed tooltips or displaying additional details as a sidenote, enhancing the communication of findings.

![Demonstration of the core features: (a) Taylor Diagram, (b) Portrait Plot, and (c) scatter plot with the side dive-down image viewer option activated. Users' mouse cursor hovering over for a specific data point (i.e., a specific ESM model and for its metrics) interactively shows a tooltip that includes detailed information, with the capability of clicking it to open the associated “dive-down” image. 

The package is built on top of the `bokeh` library. The development of `ESMBenchmarkViz` originated from the interactive visualization dashboard of the [Program for Climate Model Diagnosis and Intercomparison (PCMDI) Metrics Package](https://pcmdi.github.io/pcmdi_metrics/), showing diverse evaluation metrics for ESMs along with diagnostic information (https://pcmdi.llnl.gov/research/metrics/). We refer to these diagnostics as “dive-down information,” as they enable users to investigate metrics in greater detail.




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
