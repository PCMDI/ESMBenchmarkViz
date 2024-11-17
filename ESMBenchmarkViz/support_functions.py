# Shared support functions across the project

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from bokeh.colors import RGB
from bokeh.models import Button, CustomJS, Div, Select


def debug_print(debug: bool, str_to_print: str):
    """
    Print a string if debug is True

    Parameters
    ----------
    debug : bool
        If True, the string will be printed.
    str : str_to_print
        The string to print.
    """
    if debug:
        print(str_to_print)


def convert_to_numpy_array(data) -> np.ndarray:
    """
    Converts the input data to a numpy array if it is a list.

    Parameters
    ----------
    data : list or numpy array
        The input data.

    Returns
    -------
    numpy array
        The data converted to a numpy array.
    """
    if isinstance(data, list):
        return np.array(data)
    return data


def get_bokeh_colors_from_cmap(cmap_name: str, num_colors: int) -> list:
    """
    Generate a list of hex colors from a Matplotlib colormap for use in Bokeh.

    Parameters
    ----------
    cmap_name : str
        Name of the Matplotlib colormap.
    num_colors : int
        Number of colors to generate from the colormap.

    Returns
    -------
    list of str
        List of hex color codes that can be used in Bokeh.

    Raises
    ------
    ValueError
        If `num_colors` is less than 1.
    """
    if num_colors < 1:
        raise ValueError("num_colors must be at least 1")

    # Generate colormap from Matplotlib
    cmap = plt.get_cmap(cmap_name)
    # Generate colors and convert them to hex format
    colors = [mcolors.to_hex(cmap(i / (num_colors - 1))) for i in range(num_colors)]
    return colors


def generate_bokeh_colormap(matplotlib_cmap, num_colors, vmin=None, vmax=None):
    """
    Generate a Bokeh colormap from a Matplotlib colormap.

    This function takes a Matplotlib colormap and converts it to a list of Bokeh
    RGB colors. It allows specifying the number of colors and optional
    normalization range.

    Parameters
    ----------
    matplotlib_cmap : matplotlib.colors.Colormap
        The Matplotlib colormap to convert.
    num_colors : int
        The number of colors to generate in the Bokeh colormap.
    vmin : float, optional
        The minimum value for normalizing the colormap. If None, it defaults to
        the minimum of the data range.
    vmax : float, optional
        The maximum value for normalizing the colormap. If None, it defaults to
        the maximum of the data range.

    Returns
    -------
    list of bokeh.colors.RGB
        A list of Bokeh RGB color objects representing the converted colormap.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> from bokeh.colors import RGB
    >>> bokeh_colors = generate_bokeh_colormap(plt.get_cmap('viridis'), 10)
    >>> print(bokeh_colors)
    [RGB(68, 1, 84), RGB(72, 31, 112), ...]

    >>> # Using a different colormap with custom normalization
    >>> bokeh_colors = generate_bokeh_colormap(plt.get_cmap('plasma'), 15, vmin=0, vmax=100)
    >>> print(bokeh_colors)
    [RGB(13, 8, 135), RGB(75, 3, 161), ...]

    >>> # Using a logarithmic normalization
    >>> from matplotlib.colors import LogNorm
    >>> norm = LogNorm(vmin=1, vmax=1000)
    >>> bokeh_colors = generate_bokeh_colormap(plt.get_cmap('inferno'), 20, vmin=1, vmax=1000)
    >>> print(bokeh_colors)
    [RGB(0, 0, 4), RGB(40, 11, 84), ...]

    Notes
    -----
    This function discards the alpha channel when converting from Matplotlib
    RGB colors to Bokeh RGB colors.
    """
    # Normalize the inputs if vmin and vmax are provided
    if vmin is not None and vmax is not None:
        normalize = plt.Normalize(vmin=vmin, vmax=vmax)
    else:
        normalize = plt.Normalize()  # defaults to min/max of data

    # Generate the colors from the Matplotlib colormap
    colors = matplotlib_cmap(normalize(np.linspace(0, 1, num_colors)))

    # Convert to RGB format for Bokeh
    bokeh_colors = [RGB(*color[:3]) for color in colors]  # Discard the alpha channel

    return bokeh_colors


def create_image_display(width, height) -> Div:
    """
    Create a Bokeh Div element to display images.

    Parameters
    ----------
    width : int
        The width of the image display.
    height : int
        The height of the image display.

    Returns
    -------
    Div
        A Bokeh Div element to display images.
    """
    width = int(width)
    height = int(height)

    max_height = int(height * 0.7)
    return (
        Div(
            text="Click on a point to display the image here.",
            width=width,
            height=int(height * 0.8),
        ),
        max_height,
    )


def create_name_select(data):
    """
    Create a Bokeh Select widget to choose a data point

    Parameters
    ----------
    data : dict
        A dictionary containing the data points and their names.

    Returns
    -------
    Select
        A Bokeh Select widget to choose a data point.
    """
    return Select(
        title="Select Data Point",
        value="Select Data",
        options=["Select Data"] + data["names"],
    )


def create_navigation_buttons():
    """
    Create a Bokeh ButtonGroup to navigate between data points.

    Returns
    -------
    tuple of Button
        A tuple containing the "Previous Image" and "Next Image" buttons.
    """
    previous_button = Button(label="Previous Image", width=150)
    next_button = Button(label="Next Image", width=150)
    return previous_button, next_button


def create_dropdown_callback(source, image_display, name_select, max_height):
    """
    Create a JavaScript callback for the dropdown widget
    to update the image display and name select widgets.

    Parameters
    ----------
    source : ColumnDataSource
        The ColumnDataSource containing the data points.
    image_display : ImageDisplay
        The Div element to display images.
    name_select : Select
        The Select widget to choose a data point.
    max_height : int
        The maximum height of the image display.

    Returns
    -------
    CustomJS
        A JavaScript callback function.

    """
    return CustomJS(
        args=dict(
            source=source,
            div=image_display,
            name_select=name_select,
            maxHeight=max_height,
        ),
        code="""
            const name_value = name_select.value;
            const indices = source.data.names.map((name, i) => (name === name_value) ? i : -1).filter(i => i >= 0);

            if (indices.length > 0) {
                const selected = indices[0];
                const img_url = source.data.images[selected];
                const std_value = source.data.std_devs[selected];
                const cor_value = source.data.correlations[selected];
                const rmse_value = source.data.rmse[selected];

                if (img_url) {
                    div.text = `<a href="${img_url}" target="_blank">
                                <img src="${img_url}" style="width:100%;max-height:${maxHeight}px;height:auto;"></a>
                                <div><strong>STD:</strong> ${std_value}</div>
                                <div><strong>COR:</strong> ${cor_value}</div>
                                <div><strong>RMSE:</strong> ${rmse_value}</div>`;
                } else {
                    div.text = `<div>No image available</div>
                                <div><strong>STD:</strong> ${std_value}</div>
                                <div><strong>COR:</strong> ${cor_value}</div>
                                <div><strong>RMSE:</strong> ${rmse_value}</div>`;
                }

                // Highlight the selected point on the plot
                source.selected.indices = [selected];
            } else {
                div.text = "No matching point found.";
                source.selected.indices = [];  // Clear selection if no match
            }
            """,
    )


def create_click_callback(source, image_display, name_select, max_height):
    """
    Create a JavaScript callback function to handle click events on the plot.

    Parameters
    ----------
    source : Bokeh model
        The plot source data.
    image_display : Bokeh model
        The Div element to display images.
    name_select : Bokeh model
        The Select widget to choose a data point.
    max_height : int
        The maximum height of the image display.

    Returns
    -------
    CustomJS
        A JavaScript callback function.

    """
    return CustomJS(
        args=dict(
            source=source,
            div=image_display,
            name_select=name_select,
            maxHeight=max_height,
        ),
        code="""
            const selected = source.selected.indices[0];
            if (selected != null) {
                const name_value = source.data.names[selected];
                const img_url = source.data.images[selected];
                const std_value = source.data.std_devs[selected];
                const cor_value = source.data.correlations[selected];
                const rmse_value = source.data.rmse[selected];

                // Update dropdown
                name_select.value = name_value;

                // Update image display
                if (img_url) {
                    div.text = `<a href="${img_url}" target="_blank">
                                <img src="${img_url}" style="width:100%;max-height:${maxHeight}px;height:auto;"></a>
                                <div><strong>STD:</strong> ${std_value}</div>
                                <div><strong>COR:</strong> ${cor_value}</div>
                                <div><strong>RMSE:</strong> ${rmse_value}</div>`;
                } else {
                    div.text = `<div>No image available</div>
                                <div><strong>STD:</strong> ${std_value}</div>
                                <div><strong>COR:</strong> ${cor_value}</div>
                                <div><strong>RMSE:</strong> ${rmse_value}</div>`;
                }

            }
            """,
    )


def create_navigation_callbacks(source, image_display, name_select, max_height):
    """
    Create a JavaScript callback function to update the image display and dropdown
    when the user navigates through the data.

    Parameters
    ----------
    source : ColumnDataSource
        The ColumnDataSource containing the data.
    image_display : Div
        The Div element to display the image.
    name_select : Select
        The Select element to display the name of the selected data point.
    max_height : int
        The maximum height of the image display.

    Returns
    -------
    tuple of CustomJS
        A tuple containing the JavaScript callbacks for the "Previous Image" and "Next Image" buttons.
    """
    # JavaScript callback for "Previous Image" button
    previous_callback = CustomJS(
        args=dict(
            source=source,
            div=image_display,
            name_select=name_select,
            maxHeight=max_height,
        ),
        code="""
            let selected_index = source.selected.indices[0];
            if (selected_index !== undefined) {
                // Get the current name's index
                const current_name = source.data.names[selected_index];
                const current_index = source.data.names.indexOf(current_name);

                // Get the previous index
                const prev_index = (current_index - 1 + source.data.names.length) % source.data.names.length;
                const prev_name = source.data.names[prev_index];
                const prev_img_url = source.data.images[prev_index];
                const prev_std_value = source.data.std_devs[prev_index];
                const prev_cor_value = source.data.correlations[prev_index];
                const prev_rmse_value = source.data.rmse[prev_index];

                // Update image display
                if (prev_img_url) {
                    div.text = `<a href="${prev_img_url}" target="_blank">
                                <img src="${prev_img_url}" style="width:100%;max-height:${maxHeight}px;height:auto;"></a>
                                <div><strong>STD:</strong> ${prev_std_value}</div>
                                <div><strong>COR:</strong> ${prev_cor_value}</div>
                                <div><strong>RMSE:</strong> ${prev_rmse_value}</div>`;
                } else {
                    div.text = `<div>No image available</div>
                                <div><strong>STD:</strong> ${prev_std_value}</div>
                                <div><strong>COR:</strong> ${prev_cor_value}</div>
                                <div><strong>RMSE:</strong> ${prev_rmse_value}</div>`;
                }

                // Update dropdown
                name_select.value = prev_name;

                // Sync selection with plot
                source.selected.indices = [prev_index];
            }
            """,
    )
    # JavaScript callback for "Next Image" button
    next_callback = CustomJS(
        args=dict(
            source=source,
            div=image_display,
            name_select=name_select,
            maxHeight=max_height,
        ),
        code="""
            let selected_index = source.selected.indices[0];
            if (selected_index !== undefined) {
                // Get the current name's index
                const current_name = source.data.names[selected_index];
                const current_index = source.data.names.indexOf(current_name);

                // Get the next index
                const next_index = (current_index + 1) % source.data.names.length;
                const next_name = source.data.names[next_index];
                const next_img_url = source.data.images[next_index];
                const next_std_value = source.data.std_devs[next_index];
                const next_cor_value = source.data.correlations[next_index];
                const next_rmse_value = source.data.rmse[next_index];

                // Update image display
                if (next_img_url) {
                    div.text = `<a href="${next_img_url}" target="_blank">
                                <img src="${next_img_url}" style="width:100%;max-height:${maxHeight}px;height:auto;"></a>
                                <div><strong>STD:</strong> ${next_std_value}</div>
                                <div><strong>COR:</strong> ${next_cor_value}</div>
                                <div><strong>RMSE:</strong> ${next_rmse_value}</div>`;
                } else {
                    div.text = `<div>No image available</div>
                                <div><strong>STD:</strong> ${next_std_value}</div>
                                <div><strong>COR:</strong> ${next_cor_value}</div>
                                <div><strong>RMSE:</strong> ${next_rmse_value}</div>`;
                }

                // Update dropdown
                name_select.value = next_name;

                // Sync selection with plot
                source.selected.indices = [next_index];
            }
            """,
    )
    return previous_callback, next_callback
