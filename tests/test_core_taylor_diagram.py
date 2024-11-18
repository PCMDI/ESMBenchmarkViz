import pytest
import numpy as np
from bokeh.plotting import figure
from ESMBenchmarkViz import taylor_diagram

def test_taylor_diagram_input_validation():
    # Test for ValueError when input lists have different lengths
    std_devs = [1.0, 1.5]
    correlations = [0.9]
    names = ["Model A", "Model B"]
    refstd = 1.0
    images = ["image_a.png"]

    with pytest.raises(ValueError, match="The lengths of 'std_devs', 'correlations', and 'names' must be equal."):
        taylor_diagram(std_devs, correlations, names, refstd)

    # Test for ValueError when images are provided with mismatched lengths
    std_devs = [1.0, 1.5]
    correlations = [0.9, 0.7]
    names = ["Model A", "Model B"]
    refstd = 1.0
    images = ["image_a.png"]

    with pytest.raises(ValueError, match="The lengths of 'std_devs', 'correlations', 'names', and 'images' must be equal."):
        taylor_diagram(std_devs, correlations, names, refstd, images=images)

def test_taylor_diagram_output_type():
    std_devs = [1.0, 1.5, 2.0]
    correlations = [0.9, 0.8, 0.7]
    names = ["Model A", "Model B", "Model C"]
    refstd = 1.0

    result = taylor_diagram(std_devs, correlations, names, refstd)
    assert isinstance(result, figure), "Output should be a Bokeh figure."
