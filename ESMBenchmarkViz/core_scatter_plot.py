from typing import List, Union

import numpy as np
from bokeh.layouts import column, row
from bokeh.models import Button, ColumnDataSource, CustomJS, Div, HoverTool, Select
from bokeh.plotting import figure, show


def scatter_plot(
    x: Union[List[float], np.ndarray],
    y: Union[List[float], np.ndarray],
    names: List[str] = None,
    images: List[str] = None,
    show_plot: bool = True,
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
    show_plot : bool, optional
        If True, the plot will be displayed in the workflow (default is True).

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
    """

    # Sanity check for input data
    if len(x) != len(y) or len(x) != len(names):
        raise ValueError("Length of x, y, and names should be the same.")

    if images is not None:
        if len(x) != len(images):
            raise ValueError("Length of x, y, and images should be the same.")

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
        title="Interactive Scatter Plot",
        tools="tap, pan, wheel_zoom, box_zoom, reset",
        height=400,
        width=600,
    )
    points = p.scatter("x", "y", size=10, source=source)

    if not images:
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
        image_display = Div(
            text="Click on a point to display the image here.", width=300, height=300
        )

        max_height = 200

        # Dropdown menu for names with default "Select Data"
        name_select = Select(
            title="Select Data Point",
            value="Select Data",
            options=["Select Data"] + data["names"],
        )

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

        # Button for Previous and Next Image Navigation
        previous_button = Button(label="Previous Image", width=150)
        next_button = Button(label="Next Image", width=150)

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
