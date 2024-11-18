import numpy as np
import pytest
from bokeh.colors import RGB
from bokeh.models import CustomJS, Div, Select

from ESMBenchmarkViz.support_functions import (
    convert_to_numpy_array,
    create_click_callback,
    create_dropdown_callback,
    create_image_display,
    create_name_select,
    create_navigation_buttons,
    create_navigation_callbacks,
    debug_print,
    generate_bokeh_colormap,
    get_bokeh_colors_from_cmap,
    load_colormap,
)


def test_debug_print(capsys):
    # Test that nothing is printed when debug is False
    debug_print(False, "This should not print")
    captured = capsys.readouterr()
    assert captured.out == ""

    # Test that the string is printed when debug is True
    debug_print(True, "This should print")
    captured = capsys.readouterr()
    assert captured.out == "This should print\n"


def test_convert_to_numpy_array():
    # Test conversion from list to numpy array
    data_list = [1, 2, 3]
    result = convert_to_numpy_array(data_list)
    assert isinstance(result, np.ndarray)
    np.testing.assert_array_equal(result, np.array(data_list))

    # Test that numpy array is returned as is
    data_array = np.array([1, 2, 3])
    result = convert_to_numpy_array(data_array)
    assert result is data_array  # Should return the same object


def test_load_colormap():
    # Test loading a list of colors
    colors = ["#FF0000", "#00FF00", "#0000FF"]
    result = load_colormap(colors, 2)
    assert result == ["#FF0000", "#00FF00"]

    # Test loading a Matplotlib colormap
    result = load_colormap("viridis", 3)
    assert len(result) == 3

    # Test ValueError for insufficient colors in a list
    with pytest.raises(ValueError):
        load_colormap(colors, 4)

    # Test TypeError for invalid colormap type
    with pytest.raises(TypeError):
        load_colormap(123, 3)


def test_get_bokeh_colors_from_cmap():
    # Test valid colormap name
    result = get_bokeh_colors_from_cmap("viridis", 5)
    assert len(result) == 5

    # Test ValueError for num_colors less than 1
    with pytest.raises(ValueError):
        get_bokeh_colors_from_cmap("viridis", 0)


def test_generate_bokeh_colormap():
    from matplotlib import pyplot as plt

    # Test generating a Bokeh colormap
    bokeh_colors = generate_bokeh_colormap(plt.get_cmap("viridis"), 10)
    assert len(bokeh_colors) == 10
    assert isinstance(
        bokeh_colors[0], RGB
    )  # Check if the first color is a Bokeh RGB object


def test_create_image_display():
    width = 300
    height = 200
    div, max_height = create_image_display(width, height)
    assert isinstance(div, Div)
    assert div.width == width
    assert div.height == int(height * 0.8)
    assert max_height == int(height * 0.7)


def test_create_name_select():
    data = {"names": ["Model A", "Model B"]}
    select = create_name_select(data)
    assert isinstance(select, Select)
    assert select.title == "Select Data Point"
    assert select.options == ["Select Data"] + data["names"]


def test_create_navigation_buttons():
    previous_button, next_button = create_navigation_buttons()
    assert previous_button.label == "Previous Image"
    assert next_button.label == "Next Image"


def test_create_dropdown_callback():
    source = None  # Mocked ColumnDataSource
    image_display = None  # Mocked Div
    name_select = None  # Mocked Select
    max_height = 100

    callback = create_dropdown_callback(source, image_display, name_select, max_height)
    assert isinstance(callback, CustomJS)


def test_create_click_callback():
    source = None  # Mocked ColumnDataSource
    image_display = None  # Mocked Div
    name_select = None  # Mocked Select
    max_height = 100

    callback = create_click_callback(source, image_display, name_select, max_height)
    assert isinstance(callback, CustomJS)


def test_create_navigation_callbacks():
    source = None  # Mocked ColumnDataSource
    image_display = None  # Mocked Div
    name_select = None  # Mocked Select
    max_height = 100

    previous_callback, next_callback = create_navigation_callbacks(
        source, image_display, name_select, max_height
    )

    # Check that both callbacks are instances of CustomJS
    assert isinstance(
        previous_callback, CustomJS
    ), "Previous callback should be a CustomJS object."
    assert isinstance(
        next_callback, CustomJS
    ), "Next callback should be a CustomJS object."

    # Optionally, you can check if the code of the callbacks is not empty
    assert (
        previous_callback.code.strip() != ""
    ), "Previous callback code should not be empty."
    assert next_callback.code.strip() != "", "Next callback code should not be empty."
