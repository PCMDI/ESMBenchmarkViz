import math
from typing import List, Union

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from bokeh.colors import RGB
from bokeh.models import ColumnDataSource, HoverTool, Label, LabelSet
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap

# -------------
# Main function
# -------------


def taylor_diagram(
    std_devs: Union[List[float], np.ndarray],
    correlations: Union[List[float], np.ndarray],
    names: List[str],
    refstd: float,
    normalize: bool = False,
    step: float = 0.2,
    show_reference: bool = True,
    reference_name: str = "Reference",
    colormap: Union[str, List[str]] = "Spectral",
    width: int = 600,
    height: int = 600,
    aspect_ratio: float = 1,
    show_plot: bool = True,
    title: str = "Interactive Taylor Diagram",
) -> figure:
    """
    Creates an interactive Taylor diagram using Bokeh.

    .. image:: /_static/example_taylor_diagram.gif
        :alt: Example interactive Taylor diagram
        :align: center
        :width: 600px

    The Taylor diagram visually represents the relationship between the
    standard deviation and correlation of different models against a
    reference model. This function allows for the comparison of multiple
    models based on their standard deviations and correlations to a
    specified reference standard deviation.

    Parameters
    ----------
    std_devs : list or np.ndarray
        A list of standard deviations of the models being compared.
    correlations : list or np.ndarray
        A list of correlation coefficients of the models with respect to the reference model.
    names : list of str
        A list of names for the models being compared, used for labeling in the plot.
    refstd : float
        The standard deviation of the reference model, used for calculating RMSE and for normalization if applicable.
    normalize : bool, optional
        If True, the standard deviations are normalized by the reference standard deviation (default is False).
    step : float, optional
        The step size for the arcs and grid lines in the Taylor diagram (default is 0.2).
    show_reference : bool, optional
        If True, the reference point is shown in the Taylor diagram (default is True).
    reference_name : str, optional
        The name of the reference dataset (default is "Reference").
    colormap : str or list, optional
        A name of the `Matplotlib` or list of colors to use for the model points. Available names of `Matplotlib` colormap can be found `here <https://matplotlib.org/stable/users/explain/colors/colormaps.html>`_. Default is Spectral.
    width : int, optional
        The width of the plot in pixels (default is 600).
    height : int, optional
        The height of the plot in pixels (default is 600).
    aspect_ratio : float, optional
        The aspect ratio of the plot (default is 1).
    show_plot : bool, optional
        If True, the plot will be displayed in the workflow (default is True).
    title : str, optional
        The title of the plot (default is "Interactive Taylor Diagram").

    Returns
    -------
    bokeh.plotting.Figure
        Bokeh figure object containing the interactive Taylor diagram.

    Example
    -------
    >>> from ESMBenchmarkViz import taylor_diagram
    >>> std_devs = [0.8, 1.0, 1.2]  # Standard deviations of models
    >>> correlations = [0.9, 0.85, 0.7]  # Correlation coefficients
    >>> names = ["Model A", "Model B", "Model C"]  # Names of models
    >>> refstd = 1.0  # Standard deviation of reference model
    >>> taylor_diagram(std_devs, correlations, names, refstd)
    
    Example use case can be found `here <../examples/example_taylor_diagram.html>`_.

    Notes
    -----
    The Taylor diagram is a polar plot where the radial distance represents the standard deviation
    and the azimuthal angle represents the correlation coefficient. The reference standard deviation
    is used as a reference point for the radial distance. The correlation coefficient is represented
    by the angle between the model point and the reference point. The RMSE (Root Mean Square Error)
    is calculated as the distance between the model point and the reference point.

    2024-10-04: Jiwoo Lee, initial version

    """

    # Sanity check for input data
    if len(std_devs) != len(correlations) or len(std_devs) != len(names):
        raise ValueError(
            "The lengths of 'std_devs', 'correlations', and 'names' must be equal."
        )

    # Convert input lists to numpy arrays for consistency
    std_devs = convert_to_numpy_array(std_devs)
    correlations = convert_to_numpy_array(correlations)

    # Standard deviation axis extent
    if normalize:
        std_devs = std_devs / refstd
        refstd = 1.0
        std_name = "Normalized St. Dv."
    else:
        std_name = "Standard Deviation"

    # Add the reference to the list of models
    if show_reference:
        names.append(reference_name)
        std_devs = np.append(std_devs, refstd)
        correlations = np.append(correlations, 1.0)
        if isinstance(colormap, list):
            colormap.append("black")

    # Calculate RMSE values
    rmse = [
        np.sqrt(refstd**2 + rs**2 - 2 * refstd * rs * ts)
        for rs, ts in zip(std_devs, correlations)
    ]

    # Calculate polar coordinates
    r = std_devs
    theta = np.arccos(correlations)

    # Create figure
    max_stddev = max(std_devs)  # Get the largest standard deviation
    max_range = max_stddev * 1.1 + step  # 10% larger than the largest value
    p = figure(
        width=width,
        height=height,
        x_range=(step * -1, max_range),
        y_range=(step * -1, max_range),
        aspect_ratio=aspect_ratio,
        title=title,
    )

    p.grid.visible = False
    p.axis.visible = False

    # Apply the adjustments in your main code
    # Standard deviation and RMSE arcs
    add_reference_arcs(p, max_stddev, step=step, refstd=refstd)

    # Adjust reference lines to end at the outermost arc
    add_reference_lines(p, max_stddev + step)

    # Get the selected colormap
    if isinstance(colormap, list):
        selected_colors = colormap
    else:
        selected_colors = get_bokeh_colors_from_cmap(colormap, len(names))

    # Color mapping based on model names
    colors = factor_cmap("names", palette=selected_colors, factors=names)

    # Create a ColumnDataSource
    source = ColumnDataSource(
        data=dict(
            x=r * np.cos(theta),
            y=r * np.sin(theta),
            names=names,
            std_devs=std_devs,
            correlations=correlations,
            rmse=rmse,
        )
    )

    # Plot data points with color mapping
    points = p.scatter(
        "x", "y", size=10, source=source, color=colors, legend_field="names"
    )

    # Add labels for data points
    labels = LabelSet(
        x="x",
        y="y",
        text="names",
        x_offset=5,
        y_offset=5,
        source=source,
        text_font_size="8pt",
    )
    p.add_layout(labels)

    # Add hover tool
    hover = HoverTool(
        renderers=[points],
        tooltips=[
            ("Model", "@names"),
            (std_name, "@std_devs{0.000}"),
            ("Correlation", "@correlations{0.000}"),
            ("RMSE", "@rmse{0.000}"),
        ],
    )
    p.add_tools(hover)

    # Add axes labels with improved alignment
    p.add_layout(
        Label(
            x=max_range / 2,
            y=-0.18,
            text="Standard Deviation",
            text_font_style="italic",
            text_align="center",
        )
    )
    p.add_layout(
        Label(
            x=max_range / 1.5,
            y=max_range / 1.4,
            text="Correlation",
            text_font_style="italic",
            angle=np.deg2rad(-45),
            text_align="center",
        )
    )

    # Customize legend
    p.legend.location = "top_right"

    # Show the plot
    if show_plot:
        show(p)

    return p


# -----------------
# Support functions
# -----------------


def convert_to_numpy_array(data):
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
    RGBA colors to Bokeh RGB colors.
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


def find_circle_intersection(x1, y1, r1, x2, y2, r2):
    """
    Find the intersection points of two circles.

    Parameters
    ----------
    x1, y1 : float
        Center coordinates of the first circle.
    r1 : float
        Radius of the first circle.
    x2, y2 : float
        Center coordinates of the second circle.
    r2 : float
        Radius of the second circle.

    Returns
    -------
    list of tuple
        A list of intersection points, where each point is represented as a tuple (x, y).

    Notes
    -----
    If the circles do not intersect, or they are identical (infinite intersections),
    the function returns an empty list.

    Example
    -------
    >>> x1, y1, r1 = 0, 0, 5  # First circle: center (0, 0), radius 5
    >>> x2, y2, r2 = 4, 0, 3  # Second circle: center (4, 0), radius 3
    >>> find_circle_intersection(x1, y1, r1, x2, y2, r2)
    [(4.0, -3.0), (4.0, 3.0)]

    """
    # Distance between the centers
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # Check for no solution (the circles are too far apart or one is inside the other)
    if d > r1 + r2 or d < abs(r1 - r2):
        return []  # No intersection points

    # Check for identical circles (infinite intersections)
    if d == 0 and r1 == r2:
        return []  # Infinite intersections, return empty for now

    # Finding the intersection points
    a = (r1**2 - r2**2 + d**2) / (2 * d)
    h = math.sqrt(abs(r1**2 - a**2))

    # Finding point P2 which is the point where the line through the circle
    # intersection points crosses the line between the circle centers.
    x3 = x1 + a * (x2 - x1) / d
    y3 = y1 + a * (y2 - y1) / d

    # Now find the two intersection points
    intersection1 = (x3 + h * (y2 - y1) / d, y3 - h * (x2 - x1) / d)
    intersection2 = (x3 - h * (y2 - y1) / d, y3 + h * (x2 - x1) / d)

    return [intersection1, intersection2]


def find_circle_y_axis_intersection(x1, y1, r):
    """
    Find the intersection points of a circle and the y-axis.

    Parameters
    ----------
    x1, y1 : float
        Center coordinates of the circle.
    r : float
        Radius of the circle.

    Returns
    -------
    list of tuple
        A list of intersection points on the y-axis, where each point is represented as a tuple (0, y).
        If there are no intersections, an empty list is returned.

    Example
    -------
    >>> x1, y1, r = 3, 0, 5  # Circle center (3, 0), radius 5
    >>> find_circle_y_axis_intersection(x1, y1, r)
    [(0, 4.0), (0, -4.0)]

    """
    # Calculate the discriminant to check if there's a valid solution
    if r**2 - x1**2 < 0:
        return []  # No intersection points, circle does not reach the y-axis

    # Calculate the y values of the intersection points
    y_intersection_1 = y1 + math.sqrt(r**2 - x1**2)
    y_intersection_2 = y1 - math.sqrt(r**2 - x1**2)

    return [(0, y_intersection_1), (0, y_intersection_2)]


def angle_with_x_axis(x1, y1, x2, y2):
    """
    Calculate the angle between the line connecting two points and the x-axis.

    Parameters
    ----------
    x1, y1 : float
        Coordinates of the first point.
    x2, y2 : float
        Coordinates of the second point.

    Returns
    -------
    float
        The angle in degrees between the line connecting the two points and the x-axis.
        The angle is in the range [0, 360).

    Example
    -------
    >>> x1, y1 = 1, 1
    >>> x2, y2 = 4, 5
    >>> angle_with_x_axis(x1, y1, x2, y2)
    53.13

    """
    # Avoid division by zero in case x1 == x2 (vertical line)
    if x2 == x1:
        if y2 > y1:
            return 90.0  # Vertical line pointing upwards
        else:
            return 270.0  # Vertical line pointing downwards

    # Calculate the slope and then the angle in radians
    angle_radians = math.atan2(y2 - y1, x2 - x1)

    # Convert the angle from radians to degrees
    angle_degrees = math.degrees(angle_radians)

    # Ensure the angle is in the range [0, 360)
    if angle_degrees < 0:
        angle_degrees += 360

    return angle_degrees


def find_line_circle_intersection(x1, y1, x2, y2, x3, y3, r):
    """
    Find the intersection points of a line passing through two points and a circle.

    Parameters
    ----------
    x1, y1 : float
        Coordinates of the first point on the line.
    x2, y2 : float
        Coordinates of the second point on the line.
    x3, y3 : float
        Center coordinates of the circle.
    r : float
        Radius of the circle.

    Returns
    -------
    list of tuple
        A list of intersection points, where each point is represented as a tuple (x, y).
        If no intersection exists, the list will be empty.

    Example
    -------
    >>> x1, y1 = 1, 2  # First point on the line
    >>> x2, y2 = 4, 6  # Second point on the line
    >>> x3, y3 = 3, 3  # Center of the circle
    >>> r = 5          # Radius of the circle
    >>> intersections = find_line_circle_intersection(x1, y1, x2, y2, x3, y3, r)
    >>> print("Intersection points:", intersections)
    Intersection points: [(5.14, 7.52), (-0.74, -0.32)]

    """
    # Check if the line is vertical to avoid division by zero
    if x1 == x2:
        # Special case: Vertical line x = x1
        x = x1
        discriminant = r**2 - (x - x3) ** 2
        if discriminant < 0:
            return []  # No intersection
        y1_int = y3 + math.sqrt(discriminant)
        y2_int = y3 - math.sqrt(discriminant)
        return [(x, y1_int), (x, y2_int)]

    # Calculate the slope (m) and intercept (b) of the line
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    # Substitute the line equation y = mx + b into the circle equation (x - x3)^2 + (y - y3)^2 = r^2
    # Expand the equation and solve for x
    A = 1 + m**2
    B = 2 * (m * (b - y3) - x3)
    C = x3**2 + (b - y3) ** 2 - r**2

    # Calculate the discriminant
    discriminant = B**2 - 4 * A * C

    if discriminant < 0:
        return []  # No intersection points

    # Calculate the x values of the intersection points
    x_int1 = (-B + math.sqrt(discriminant)) / (2 * A)
    x_int2 = (-B - math.sqrt(discriminant)) / (2 * A)

    # Calculate the corresponding y values using the line equation y = mx + b
    y_int1 = m * x_int1 + b
    y_int2 = m * x_int2 + b

    return [(x_int1, y_int1), (x_int2, y_int2)]


# Function to add reference arcs and labels (Standard deviation and RMSE) on Taylor Diagram
def add_reference_arcs(plot, max_stddev, step, refstd=1, thick_refstd=True):
    """Adds reference arcs for standard deviation and RMSE to the plot."""
    loop_range = np.arange(step, max_stddev + 2 * step, step)
    outermost_radius = loop_range[-1]

    for n, i in enumerate(loop_range):
        if n < len(loop_range) - 1:
            # inner arcs
            line_color = "gray"
            line_width = 1
        else:
            # outermost arc
            line_color = "black"
            line_width = 3

        # ======================
        # Standard deviation arc
        # ======================
        plot.arc(
            0,
            0,
            radius=i,
            start_angle=0,
            end_angle=np.pi / 2,
            color=line_color,
            line_dash="solid",
            alpha=0.3,
            line_width=line_width,
        )
        label = Label(
            x=i + 0.05,
            y=0,
            text=f"{i:.1f}",
            text_font_size="10pt",
            text_align="right",
            text_alpha=0.7,
            x_offset=0,
            y_offset=-12,
        )
        plot.add_layout(label)

        # ========
        # RMSE arc
        # ========
        # To make RMSE arc starts from the outermost standard deviation arc,
        # find intersection with outermost standard deviation arc and RMSE arc
        intersections_start = find_circle_intersection(
            refstd, 0, i, 0, 0, outermost_radius
        )

        # Basic start and end angle: 0 deg to 180 deg
        start_angle = 0
        end_angle = np.pi

        # Update start angle if there is intersection of the outermost standard deviation arc and the RMSE arc
        if len(intersections_start) > 0:
            for intersection in intersections_start:
                x_i = intersection[0]
                y_i = intersection[1]
                if x_i > 0 and y_i > 0:
                    start_angle = np.deg2rad(angle_with_x_axis(refstd, 0, x_i, y_i))

        # To make RMSE arc ends at y-axis,
        # find intersection with y-axis and update end angle
        intersections_end = find_circle_y_axis_intersection(refstd, 0, i)

        if len(intersections_end) > 0:
            for intersection in intersections_end:
                y_i = intersection[1]
                if y_i > 0:
                    end_angle = np.deg2rad(angle_with_x_axis(refstd, 0, 0, y_i))

        # Plot actual RMSE arc
        plot.arc(
            refstd,
            0,
            radius=i,
            start_angle=start_angle,
            end_angle=end_angle,
            color="gray",
            line_dash="dashed",
            alpha=0.3,
        )

    # Add labels on RMSE arcs
    add_rmse_labels(plot, loop_range, refstd)

    if thick_refstd:
        # Make the reference standard deviation arc more noticeable using thicker line
        plot.arc(
            0,
            0,
            radius=refstd,
            start_angle=0,
            end_angle=np.pi / 2,
            color="black",
            line_dash="solid",
            alpha=0.3,
            line_width=2,
        )


# Function to add RMSE labels on Taylor Diagram
def add_rmse_labels(plot, rmse_values, refstd):
    """Adds labels along RMSE arcs following a virtual line that passes the center of RMSE arc and upper-left corner of the plot"""
    for rmse_value in rmse_values:
        # Find intersections of RMSE arc and the virtual line, then find crossing angle
        intersections = find_line_circle_intersection(
            refstd, 0, 0, rmse_values[-1], refstd, 0, rmse_value
        )

        for intersection in intersections:
            if len(intersection) > 0 and intersection[0] > 0 and intersection[1] > 0:
                x = intersection[0]
                y = intersection[1]
                angle_deg = angle_with_x_axis(refstd, 0, x, y) - 90
            else:
                # just in case something fails use the below values
                x = (
                    1 - rmse_value / 2
                )  # Adjust x-coordinate for label placement along the RMSE arc
                y = (
                    rmse_value / 1.18
                )  # Adjust y-coordinate for label placement along the RMSE arc
                angle_deg = 40

        label = Label(
            x=x,
            y=y,
            text=f"{rmse_value:.2f}",
            text_font_size="8pt",
            text_align="center",
            text_alpha=0.7,
            angle=np.deg2rad(angle_deg),
        )
        plot.add_layout(label)


# Function to add reference lines for correlation on Taylor Diagram
def add_reference_lines(plot, max_radius):
    """Adds reference correlation lines to the plot that end at the max radius (outermost standard deviation arc)."""
    rlocs = np.flip(np.concatenate((np.arange(10) / 10.0, [0.95, 0.99, 1])))
    tlocs = np.arccos(rlocs)

    for angle, correlation in zip(tlocs, rlocs):
        if angle == 0 or angle == np.pi / 2:
            line_color = "black"
            line_width = 3
            line_dash = "solid"
        else:
            line_color = "gray"
            line_width = 1
            line_dash = "dotted"
        x = max_radius * correlation
        y = max_radius * np.sin(angle)
        plot.line(
            [0, x],
            [0, y],
            color=line_color,
            line_dash=line_dash,
            alpha=0.3,
            line_width=line_width,
        )
        label = Label(
            x=x,
            y=y,
            text=f"{correlation}",
            text_font_size="8pt",
            text_align="left",
            text_alpha=0.7,
            x_offset=5,
            y_offset=5,
        )
        plot.add_layout(label)
