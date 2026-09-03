from copy import deepcopy
from typing import List, Union

import numpy as np
from bokeh.io import export_png
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CustomJS, HoverTool
from bokeh.plotting import figure, show

from .support_functions import (
    create_image_display,
    create_name_select,
    create_navigation_buttons,
)


def scatter_plot(
    x: Union[List[float], np.ndarray],
    y: Union[List[float], np.ndarray],
    names: List[str] = None,
    images: List[str] = None,
    show_image_panel: bool = False,
    title: str = "Interactive Scatter Plot",
    width: int = 600,
    height: int = 400,
    show_plot: bool = True,
    static: bool = False,
    static_filename: str = "./scatter_plot.png",
    bokeh_logo: bool = True,
    debug: bool = False,
) -> figure:
    """
    Create an interactive scatter plot with tooltips, dropdown, and an image display.

    Parameters
    ----------
    x : list or np.ndarray
        List of x-coordinates values.
    y : list or np.ndarray
        List of y-coordinates values.
    names : list
        List of names corresponding to the data points.
    images : list, optional
        List of image file paths corresponding to the data points, by default None
    show_image_panel : bool, optional
        If True and images are provided, displays the interactive image panel on the right side.
        If False, images appear only in tooltips without the panel. Default is False.
    title : str, optional
        Title of the plot, by default "Interactive Scatter Plot"
    width : int, optional
        Width of the plot, by default 600
    height : int, optional
        Height of the plot, by default 400
    show_plot : bool, optional
        If True, the plot will be displayed in the workflow (default is True).
    static : bool, optional
        If True, exports the plot as a static PNG file to the path specified by static_filename.
        Default is False.
    static_filename : str, optional
        The file path where the static PNG will be saved when static=True.
        Default is "./scatter_plot.png".
    bokeh_logo : bool, optional
        If True, displays the Bokeh logo in the plot. Default is True.
    debug : bool, optional
        If True, prints additional debugging information. Default is False.

    Returns
    -------
    bokeh.plotting.Figure or bokeh.layouts.layout
        The layout containing the scatter plot and controls.

    Example
    -------
    >>> from ESMBenchmarkViz import scatter_plot
    >>> x = [1, 2, 3]
    >>> y = [6, 7, 2]
    >>> names = ["A", "B", "C"]
    >>> images = ["images/image1.jpg", "images/image2.jpg", "images/image3.jpg"]
    >>> scatter_plot(x, y, names, images)

    Example use case can be found `here <../examples/example_scatter_plot.html>`_.

    Notes
    -----
    2024-11-18: Jiwoo Lee, initial version
    """

    # Sanity check for input data
    if len(x) != len(y) or len(x) != len(names):
        raise ValueError("Length of x, y, and names should be the same.")

    if images is not None:
        if len(x) != len(images):
            raise ValueError("Length of x, y, and images should be the same.")

    # Use deepcopy to prevent modifying user's input lists
    if names is not None:
        names = deepcopy(names)
    if images is not None:
        images = deepcopy(images)

    # Wrap up input as a dictionary
    data = {
        "x": x,
        "y": y,
        "names": names,
    }

    if images:
        data["images"] = images

    source = ColumnDataSource(data=data)

    # Create a scatter plot
    p = figure(
        width=width,
        height=height,
        title=title,
        tools="tap, pan, wheel_zoom, box_zoom, reset, save",
    )
    points = p.scatter("x", "y", size=10, source=source)

    # Control Bokeh logo display
    if bokeh_logo is False:
        p.toolbar.logo = None

    if not images or not show_image_panel:
        # Add hover tool (with or without images in tooltips)
        if images:
            # Images in tooltips only, no panel
            hover = HoverTool(
                renderers=[points],
                tooltips="""
                    <div>
                        <img src="@images" alt="" style="width:100px;height:auto;"/>
                        <div><strong>Name:</strong> @names</div>
                        <div><strong>X:</strong> @x</div>
                        <div><strong>Y:</strong> @y</div>
                    </div>
                    """,
            )
        else:
            # Text-only tooltips
            hover = HoverTool(
                renderers=[points],
                tooltips=[
                    ("Name", "@names"),
                    ("X", "@x"),
                    ("Y", "@y"),
                ],
            )
        p.add_tools(hover)
        return_object = p

    else:
        # Images with interactive panel
        # Add hover tool with image tooltip
        hover = HoverTool(
            renderers=[points],
            tooltips="""
                <div>
                    <img src="@images" alt="" style="width:100px;height:auto;"/>
                    <div><strong>Name:</strong> @names</div>
                    <div><strong>X:</strong> @x</div>
                    <div><strong>Y:</strong> @y</div>
                </div>
                """,
        )
        p.add_tools(hover)

        # Div to display image and x, y values on click
        # maximum height is for the actual image display inside the image_display Div
        image_display, max_height = create_image_display(width, height)

        # Dropdown menu for names with default "Select Data"
        name_select = create_name_select(data)

        # Create buttons for Previous and Next Image Navigation
        previous_button, next_button = create_navigation_buttons()

        # JavaScript callback for dropdown selection changes
        dropdown_callback = CustomJS(
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
                const x_value = source.data.x[selected];
                const y_value = source.data.y[selected];

                if (img_url) {
                    div.text = `<a href="${img_url}" target="_blank"><img src="${img_url}" style="width:100%;max-height:${maxHeight}px;height:auto;"></a><div><strong>X:</strong> ${x_value}</div><div><strong>Y:</strong> ${y_value}</div>`;
                } else {
                    div.text = `<div>No image available</div><div><strong>X:</strong> ${x_value}</div><div><strong>Y:</strong> ${y_value}</div>`;
                }

                // Highlight the selected point on the scatter plot
                source.selected.indices = [selected];
            } else {
                div.text = "No matching point found.";
                source.selected.indices = [];  // Clear selection if no match
            }
        """,
        )
        name_select.js_on_change("value", dropdown_callback)

        # JavaScript callback for click events
        click_callback = CustomJS(
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
                const x_value = source.data.x[selected];
                const y_value = source.data.y[selected];

                // Update dropdown
                name_select.value = name_value;

                if (img_url) {
                    // Display the image
                    div.text = `<a href="${img_url}" target="_blank"><img src="${img_url}" style="width:100%;max-height:${maxHeight}px;height:auto;"></a><div><strong>X:</strong> ${x_value}</div><div><strong>Y:</strong> ${y_value}</div>`;
                } else {
                    // No image available
                    div.text = `<div>No image available</div><div><strong>X:</strong> ${x_value}</div><div><strong>Y:</strong> ${y_value}</div>`;
                }
            }
        """,
        )
        source.selected.js_on_change("indices", click_callback)

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
                const prev_x = source.data.x[prev_index];
                const prev_y = source.data.y[prev_index];

                if (prev_img_url) {
                    // Update image and x, y values
                    div.text = `<a href="${prev_img_url}" target="_blank"><img src="${prev_img_url}" style="width:100%;max-height:${maxHeight}px;height:auto;"></a><div><strong>X:</strong> ${prev_x}</div><div><strong>Y:</strong> ${prev_y}</div>`;
                } else {
                    div.text = `<div>No image available</div><div><strong>X:</strong> ${prev_x}</div><div><strong>Y:</strong> ${prev_y}</div>`;
                }
                name_select.value = prev_name;

                // Sync selection with plot
                source.selected.indices = [prev_index];
            }
        """,
        )
        previous_button.js_on_event("button_click", previous_callback)

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
                const next_x = source.data.x[next_index];
                const next_y = source.data.y[next_index];

                if (next_img_url) {
                    // Update image and x, y values
                    div.text = `<a href="${next_img_url}" target="_blank"><img src="${next_img_url}" style="width:100%;max-height:${maxHeight}px;height:auto;"></a><div><strong>X:</strong> ${next_x}</div><div><strong>Y:</strong> ${next_y}</div>`;
                } else {
                    div.text = `<div>No image available</div><div><strong>X:</strong> ${next_x}</div><div><strong>Y:</strong> ${next_y}</div>`;
                }
                name_select.value = next_name;

                // Sync selection with plot
                source.selected.indices = [next_index];
            }
        """,
        )
        next_button.js_on_event("button_click", next_callback)

        # Arrange the Previous and Next buttons side by side
        navigation_buttons = row(previous_button, next_button)

        # Arrange layout
        controls = column(name_select, image_display, navigation_buttons)
        layout = row(p, controls)

        return_object = layout

    # Export static PNG if requested
    if static:
        try:
            export_png(return_object, filename=static_filename)
            if debug:
                print(f"Static PNG exported to {static_filename}")
        except Exception as e:
            print(f"Failed to export PNG: {e}")
            print(
                "Tip: Install selenium and a browser driver (e.g., chromedriver) for PNG export"
            )

    if show_plot:
        show(return_object)

    return return_object


if __name__ == "__main__":
    # Example usage
    x = [1, 2, 3]
    y = [6, 7, 2]
    names = ["Point A", "Point B", "Point C"]
    images = [
        "images/image1.jpg",  # Example of a valid image URL
        None,  # Example of no image (None value)
        "images/image3.jpg",  # Example of another valid image URL
    ]

    # Create the plot layout
    layout = scatter_plot(x, y, names, images=images)

    # Add layout to the current document
    # curdoc().add_root(layout)
    # show(layout)
