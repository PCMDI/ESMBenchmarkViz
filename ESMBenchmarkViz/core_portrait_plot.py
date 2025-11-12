# - Generate an interactive Portrait Plot using Bokeh.
# - Author: Jiwoo Lee (2021.08)
# - Last update: 2025.08 (Kristin Chang)

import math
import sys
from copy import deepcopy
from typing import List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bokeh.colors import RGB
from bokeh.io import export_png
from bokeh.models import (
    BasicTicker,
    ColorBar,
    ColumnDataSource,
    LinearAxis,
    LinearColorMapper,
    OpenURL,
    Patches,
    TapTool,
    Span
)
from bokeh.plotting import figure, show

# -------------
# Main function
# -------------


def portrait_plot(
    data: Union[np.ndarray, List[np.ndarray]],
    xaxis_labels: List[str],
    yaxis_labels: List[str],
    width: Union[int, str] = 600,
    height: Union[int, str] = 600,
    glyph_rows: Optional[int] = None,
    static: bool = False,
    static_filename: str = "./static_portrait_plot.png",
    annotate: bool = False,
    annotate_data: Optional[np.ndarray] = None,
    vrange: Optional[Tuple[float, float]] = None,
    xaxis_fontsize: Optional[int] = None,
    yaxis_fontsize: Optional[int] = None,
    xaxis_fontstyle: Optional[str] = None,
    yaxis_fontstyle: Optional[str] = None,
    xaxis_location: str = "above",
    xaxis_rotation: int = 45,
    title: Optional[str] = None,
    cmap: str = "RdBu_r",
    cmap_bounds: Optional[List[float]] = None,
    cbar_place: str = "right",
    cbar_tick_fontsize: Optional[int] = None,
    invert_yaxis: bool = True,
    clickable: bool = False,
    line_color: str = "grey",
    legend_name: Optional[str] = "Group",
    legend_labels: Optional[List[str]] = None,
    img_url: Optional[List[str]] = None,
    tooltips: Optional[Union[str, List[Tuple[str, str]]]] = None,
    url_open: Optional[List[str]] = None,
    missing_color: str = "grey",
    aspect_scale: float = 1,
    show_plot: bool = True,
    bokeh_toolbar: bool = True,
    bokeh_logo: bool = True,
    debug: bool = False,
):
    """
    Generates an interactive portrait plot using Bokeh.

    Parameters
    ----------
    data : numpy.ndarray or list of numpy.ndarray
        A 2D array, a list of 2D arrays, or a 3D array (stacked 2D arrays) containing the data to plot.
    xaxis_labels : list of str
        Labels for the x-axis. The number of labels must match the x-axis dimensions, or use an empty list to disable labels.
    yaxis_labels : list of str
        Labels for the y-axis. The number of labels must match the y-axis dimensions, or use an empty list to disable labels.
    width : int, optional
        Width of the plot in pixels. Default is 600. If 'auto', the width is calculated based on the data size.
    height : int, optional
        Height of the plot in pixels. Default is 600. If 'auto', the height is calculated based on the data size.
    annotate : bool, optional
        If True, adds annotations to the plot (only for heatmap-style plots). Default is False.
    annotate_data : numpy.ndarray, optional
        A 2D array to use for annotations. If None, `data` is used. Default is None.
    vrange : tuple of float, optional
        Range of values for the color scale. Default is None.
    xaxis_fontsize : int, optional
        Font size for the x-axis tick labels. Default is None.
    yaxis_fontsize : int, optional
        Font size for the y-axis tick labels. Default is None.
    xaxis_fontstyle : str, optional
        Font style for the x-axis labels. Options are ['normal', 'italic', 'bold', 'bold italic']. Default is None.
    yaxis_fontstyle : str, optional
        Font style for the y-axis labels. Options are ['normal', 'italic', 'bold', 'bold italic']. Default is None.
    xaxis_location : str, optional
        Location of the x-axis. Options are ['above', 'below', 'both']. Default is 'above'.
    xaxis_rotation : int, optional
        Rotation angle of the x-axis tick labels in degrees. Default is 45.
    title : str, optional
        Title of the figure. Default is None.
    cmap : str, optional
        Name of the matplotlib colormap to use. Default is 'RdBu_r'.
    cmap_bounds : list of float, optional
        If specified, applies discrete color bins. Default is None.
    cbar_place : str, optional
        Location of the colorbar. Options are ['left', 'right', 'above', 'below', 'center']. Default is 'right'.
    cbar_tick_fontsize : int, optional
        Font size for the colorbar tick labels. Default is None.
    invert_yaxis : bool, optional
        If True, places y=0 at the top of the plot. Default is True.
    clickable : bool, optional
        If True, enables clickable functionality. Default is False.
    line_color: str, optional
        Color of the lines in the plot. Default is 'grey'.
    legend_name: str, optional
        Name of the legend (used for triangular plots). Default is 'Group'.
    legend_labels : list of str, optional
        Labels for the legend (used for triangular plots). Default is None.
    img_url : list of str, optional
        Links to images displayed in tooltips. Default is None.
    tooltips : str or list of tuple, optional
        Tooltips for the plot. Default is None.
    url_open : list of str, optional
        Links to open when a tooltip is clicked. Default is None.
    missing_color : str, optional
        Color for missing values in the plot. Default is 'grey'.
    aspect_scale : float, optional
        Scale factor for the plot aspect ratio. Default is 1.
    show_plot : bool, optional
        If True, the plot will be displayed in the workflow (default is True).
    bokeh_toolbar : bool, optional
        If True, displays the Bokeh toolbar in the plot. Default is True.
    bokeh_logo : bool, optional
        If True, displays the Bokeh logo in the plot. Default is True.
    debug : bool, optional
        If True, prints debug messages. Default is False.

    Returns
    -------
    plot : Bokeh component
        A Bokeh plot object representing the interactive portrait plot.

    Example
    -------
    >>> from ESMBenchmarkViz import portrait_plot

    Notes
    -----
    - The function supports both 2D and stacked 3D data for generating portrait plots.
    - Interactive features include tooltips and clickable URLs, enabled through Bokeh.
    - Missing values are displayed using the specified `missing_color`.
    """

    # ----------------
    # Prepare plotting
    # ----------------
    data, num_divide = prepare_data(data, xaxis_labels, yaxis_labels, debug)

    if annotate:
        annotate_data, num_divide_annotate = prepare_data(
            annotate_data, xaxis_labels, yaxis_labels, debug
        )
        if num_divide_annotate != num_divide:
            sys.exit("Error: annotate_data does not have same size as data")

    if url_open is None:
        url_open = img_url

    # Figure type
    if num_divide > 1 and len(data.shape) == 3:
        if num_divide != len(data):
            sys.exit("Error: data.shape[0] is not equal to num_divide")
        if annotate:
            if num_divide != len(annotate_data):
                sys.exit("Error: annotate_data.shape[0] is not equal to num_divide")

    if glyph_rows:
        xpts_list, ypts_list, positions = get_glyph_row_points(glyph_rows)
    else:
        xpts_list, ypts_list = get_x_y_points(num_divide)
        positions = get_positions(num_divide)

    # Prepare data for plotting
    # ~~~~~~~~~~~~~~~~~~~~~~~~~
    xs, ys = list(), list()
    field, field2 = list(), list()
    positions_list, position_description_list = list(), list()
    xname_list, yname_list = list(), list()

    for i in range(num_divide):
        xpts = xpts_list[i]
        ypts = ypts_list[i]
        if num_divide > 1 and len(data.shape) == 3:
            a = data[i].copy()
            if annotate:
                annotate_a = annotate_data[i].copy()
        elif num_divide == 1 and len(data.shape) == 2:
            a = data.copy()
            if annotate:
                annotate_a = annotate_data.copy()
        else:
            sys.exit("Error: data.shape is not right")

        y = list(range(0, a.shape[0]))
        x = list(range(0, a.shape[1]))

        if invert_yaxis:
            a = np.flipud(deepcopy(a))
            if annotate:
                annotate_a = np.flipud(deepcopy(annotate_a))

        # xs, ys: x- and y-coordinates for all the patches,
        # given as a “list of lists”.
        for iy in y:
            yname = yaxis_labels[iy]
            for ix in x:
                xname = xaxis_labels[ix]
                xs.append([tmp_x + ix for tmp_x in xpts])
                ys.append([tmp_y + iy for tmp_y in ypts])
                field.append(a[iy, ix])
                if annotate:
                    field2.append(annotate_a[iy, ix])
                if legend_labels is not None:
                    position_description_list.append(legend_labels[i])
                if positions is not None:
                    positions_list.append(positions[i])
                xname_list.append(xname)
                yname_list.append(yname)

    # Gathered data for plotting
    col_dict = dict(
        xs=xs,
        ys=ys,
        field=field,
        xname=xname_list,
        yname=yname_list,
    )

    # if img_url is not None, update col_dict with img_url
    if img_url is not None:
        col_dict.update(dict(img=img_url))

    # if url_open is not None, update col_dict with url_open
    if url_open is not None:
        col_dict.update(dict(url=url_open))

    # if field2 is not empty, update col_dict with field2
    if len(field2) > 0:
        col_dict.update(dict(field2=field2))
        col_dict_df = pd.DataFrame.from_dict(col_dict)
        col_dict_df.loc[col_dict_df.field2.isna(), ("img")] = (
            "https://pcmdi.llnl.gov/pmp-preliminary-results/interactive_plot/mean_climate/no-data-whitebg.png"
        )
        col_dict.update(dict(img=col_dict_df["img"].tolist()))

    # if position_list is not None, update col_dict with position_list
    if len(positions_list) == len(xname_list):
        col_dict.update(dict(position=positions_list))

    # if position_description_list is not empty, update col_dict with position_description_list
    if len(position_description_list) > 0:
        col_dict.update(dict(position_description=position_description_list))

    if debug:
        print("col_dict: ", col_dict)
        print("col_dict.keys(): ", col_dict.keys())
        print("col_dict['xs']: ", col_dict["xs"])
        print("col_dict['ys']: ", col_dict["ys"])
        print("col_dict['position']: ", col_dict["position"])

    source = ColumnDataSource(col_dict)

    # ----------------
    # Ready to plot!!
    # ----------------
    # Figure size
    if width == "auto":
        plot_width = data.shape[-1] * 30 + 150
    else:
        plot_width = width

    if height == "auto":
        plot_height = data.shape[-2] * 30
    else:
        plot_height = height

    # yaxis starts from top
    if invert_yaxis:
        yaxis_labels = deepcopy(yaxis_labels)[::-1]

    if clickable:
        tools = "hover, tap, save"  # hover needed for tooltip, tap needed for url open
    else:
        tools = "hover, save"

    if img_url is not None:
        if tooltips is None:
            # Customized tooltip
            tooltips = """
                <div>
                    <div>
                        <img
                            src="@img" alt="@img" width="300" height="200"
                            style="float: left; margin: 0px 5px 5px 0px;"
                            border="1"
                            onerror
                            style="margin: -75px 0 0 -100px"
                        ></img><br>
                        <span style="font-size: 14px">
                        <font color=darkgreen>Model:</font> <b>@yname</b><br>
                        <font color=darkgreen>Variable:</font> <b>@xname</b><br>"""

            if len(position_description_list) > 0:
                tooltips += f"<font color=darkgreen>{legend_name.capitalize()}:</font> <b>@position_description</b><br>"

            tooltips += """
                        <font color=darkgreen>Value (Nor.):</font> @field<br>
                        <font color=darkgreen>Value (Act.):</font> @field2</span>
                    </div>
                </div>"""
    else:
        if tooltips is None:
            tooltips = [("Model", "@yname"), ("Variable", "@xname")]

            if len(position_description_list) > 0:
                tooltips.append((legend_name.capitalize(), "@position_description"))

            tooltips += [
                ("Value (Nor.)", "@field"),
            ]
            if annotate:
                tooltips.append(("Value (Act.)", "@field2"))

            if debug and num_divide > 1:
                tooltips.append(("Position", "@position"))

    if xaxis_location in ["above", "below"]:
        x_axis_location = xaxis_location
    elif xaxis_location == "both":
        x_axis_location = "above"
    else:
        sys.exit("Error: xaxis_location should be either above, below, or both")

    if static:
        plot = figure(
            title=title,
            x_range=xaxis_labels,
            y_range=yaxis_labels,
            width=plot_width,
            height=plot_height,
            min_border=50,
            x_axis_location=x_axis_location,
            aspect_scale=aspect_scale,
        )
    else:
        plot = figure(
            title=title,
            x_range=xaxis_labels,
            y_range=yaxis_labels,
            width=plot_width,
            height=plot_height,
            min_border=50,
            tools=tools,
            tooltips=tooltips,
            x_axis_location=x_axis_location,
            aspect_scale=aspect_scale,
        )

    # Color Map control
    if cmap_bounds is None:
        ncolors = 255
    else:
        ncolors = len(cmap_bounds) - 1

    colormap = plt.get_cmap(cmap, ncolors)
    m_colormap_rgb = (255 * colormap(range(0, ncolors))).astype("int")
    colors = [RGB(*tuple(rgb)).to_hex() for rgb in m_colormap_rgb]

    if vrange is None:
        vmin = np.nanmin(np.array(field))
        vmax = np.nanmax(np.array(field))
    else:
        vmin = np.min(vrange)
        vmax = np.max(vrange)

    if cmap_bounds is not None:
        vmin = min([vmin, min(cmap_bounds)])
        vmax = max([vmax, max(cmap_bounds)])

    mapper = LinearColorMapper(
        palette=colors, low=vmin, high=vmax, nan_color=missing_color
    )

    glyph = Patches(
        xs="xs",
        ys="ys",
        fill_color={"field": "field", "transform": mapper},
        line_color=line_color,
        line_width=0.5,
    )

    # Generate actual plot
    plot.add_glyph(
        source, glyph, selection_glyph=glyph, nonselection_glyph=glyph
    )  # keep same transparency regardless of selection

    # x-axis tick labels
    plot.xaxis.major_label_orientation = math.radians(
        xaxis_rotation
    )  # degree to radian
    if xaxis_fontsize is not None:
        plot.xaxis.major_label_text_font_size = str(xaxis_fontsize) + "pt"
    if xaxis_fontstyle is not None:
        plot.xaxis.major_label_text_font_style = xaxis_fontstyle
    # y-axis tick labels
    if yaxis_fontsize is not None:
        plot.yaxis.major_label_text_font_size = str(yaxis_fontsize) + "pt"
    if yaxis_fontstyle is not None:
        plot.yaxis.major_label_text_font_style = yaxis_fontstyle

    # x-axis at the bottom as well
    if xaxis_location == "both" and x_axis_location == "above":
        plot.add_layout(LinearAxis(), "below")
        plot.xaxis[1].ticker = [x + 0.5 for x in list(range(0, len(xaxis_labels)))]
        xaxis_dict = dict()
        for x in list(range(0, len(xaxis_labels))):
            xaxis_dict[x + 0.5] = xaxis_labels[x]
        plot.xaxis[1].major_label_overrides = xaxis_dict
        plot.xaxis[1].major_label_orientation = math.radians(
            xaxis_rotation
        )  # degree to radian
        if xaxis_fontsize is not None:
            plot.xaxis[1].major_label_text_font_size = str(xaxis_fontsize) + "pt"
        if xaxis_fontstyle is not None:
            plot.xaxis[1].major_label_text_font_style = xaxis_fontstyle

    # Color Bar
    if cbar_tick_fontsize is None:
        cbar_tick_fontsize = "12px"
    else:
        cbar_tick_fontsize = str(int(cbar_tick_fontsize)) + "px"

    color_bar = ColorBar(
        color_mapper=mapper,
        major_label_text_font_size=cbar_tick_fontsize,
        ticker=BasicTicker(desired_num_ticks=10),
        label_standoff=6,
        border_line_color=None,
        location=(0, 0),
    )
    plot.add_layout(color_bar, cbar_place)

    # if using glyph rows, add borders
    if glyph_rows:
        line_locations = np.arange(0, len(yaxis_labels)+1, 1)
        for loc in line_locations:
            h_lines = Span(location=loc, dimension='width', line_color='black', line_width=2)
            plot.add_layout(h_lines)

    # Link to open when clicked
    if clickable:
        taptool = plot.select(type=TapTool)
        taptool.callback = OpenURL(url="@url")

    # Trun off bokeh log
    if bokeh_logo is False:
        plot.toolbar.logo = None

    # Turn off bokeh toolbar
    if static:
        bokeh_toolbar = False
    if bokeh_toolbar is False:
        plot.toolbar_location = None

    # Title
    if title is not None:
        plot.title.align = "center"

    return_object = plot

    # Show the plot if requested
    if show_plot:
        show(return_object)

    # if static, export plot as png
    if static:
        export_png(plot, filename=static_filename)

    return return_object


# -----------------
# Support functions
# -----------------


def prepare_data(data, xaxis_labels, yaxis_labels, debug=False):
    """
    Prepare data for plotting.

    Parameters
    ----------
    data : list or np.ndarray
        Data to plot.
    xaxis_labels : list of str
        Labels for the x-axis.
    yaxis_labels : list of str
        Labels for the y-axis.
    debug : bool, optional
        If True, print debug information. The default is False.

    Returns
    -------
    np.ndarray, int
        The data and the number of divisions.
    """
    # In case data was given as list of arrays, convert it to numpy (stacked) array
    if isinstance(data, list):
        if debug:
            print("data type is list")
            print("len(data):", len(data))
        if len(data) == 1:  # list has only 1 array as element
            if isinstance(data[0], np.ndarray) and (len(data[0].shape) == 2):
                data = data[0]
                num_divide = 1
            else:
                sys.exit("Error: Element of given list is not in np.ndarray type")
        else:  # list has more than 1 arrays as elements
            data = np.stack(data)
            num_divide = len(data)

    # Now, data is expected to be be a numpy array (whether given or converted from list)
    if debug:
        print("data.shape:", data.shape)

    if data.shape[-1] != len(xaxis_labels) and len(xaxis_labels) > 0:
        sys.exit("Error: Number of elements in xaxis_label mismatchs to the data")

    if data.shape[-2] != len(yaxis_labels) and len(yaxis_labels) > 0:
        sys.exit("Error: Number of elements in yaxis_label mismatchs to the data")

    if isinstance(data, np.ndarray):
        # data = np.squeeze(data)
        if len(data.shape) == 2:
            num_divide = 1
        elif len(data.shape) == 3:
            num_divide = data.shape[0]
        else:
            print("data.shape:", data.shape)
            sys.exit("Error: data.shape is not right")
    else:
        sys.exit("Error: Converted or given data is not in np.ndarray type")

    if debug:
        print("num_divide:", num_divide)

    return data, num_divide


def find_intersection_points_centered(num_sectors: int) -> list:
    """
    Finds intersection points of evenly spaced radius lines from the center of a circle
    with a square on the x-y plane. The first partition is centered at angle 90° (π/2 radians),
    regardless of whether the number of sectors is odd or even.

    Parameters
    ----------
    num_sectors : int
        Number of sectors to divide the circle into.

    Returns
    -------
    list of tuples
        Intersection points of the radius lines with the square boundary.
    """
    if num_sectors < 2:
        raise ValueError("Number of sectors must be greater than 1.")

    if num_sectors == 2:
        return [(0, 0), (1, 1)]

    # Define square edges
    edges = [
        ((0, 0), (1, 0)),  # Bottom edge
        ((1, 0), (1, 1)),  # Right edge
        ((1, 1), (0, 1)),  # Top edge
        ((0, 1), (0, 0)),  # Left edge
    ]

    # Circle center and radius
    center = (0.5, 0.5)
    radius = 0.5

    # Calculate evenly spaced angles in the clockwise direction
    angles = np.linspace(
        0, -2 * np.pi, num_sectors, endpoint=False
    )  # Negative to reverse direction
    if num_sectors % 2 == 0:
        # Shift angles to center the first sector at 90° (π/2)
        angles = angles - (angles[1] / 2) + np.pi / 2
    else:
        # Shift angles for odd sectors to ensure first centered at 90° (π/2)
        angles = angles + np.pi / num_sectors + np.pi / 2

    intersection_points = []

    for angle in angles:
        # Define the line direction from the center
        dx, dy = np.cos(angle), np.sin(angle)
        ray_end = (center[0] + dx * radius, center[1] + dy * radius)

        for edge in edges:
            (x1, y1), (x2, y2) = edge

            # Solve line-line intersection
            det = (x1 - x2) * (center[1] - ray_end[1]) - (y1 - y2) * (
                center[0] - ray_end[0]
            )
            if det == 0:
                continue

            t = (
                (x1 - center[0]) * (center[1] - ray_end[1])
                - (y1 - center[1]) * (center[0] - ray_end[0])
            ) / det
            u = -((x1 - x2) * (y1 - center[1]) - (y1 - y2) * (x1 - center[0])) / det

            if 0 <= t <= 1 and u >= 0:
                ix = x1 + t * (x2 - x1)
                iy = y1 + t * (y2 - y1)
                intersection_points.append((ix, iy))
                break

    return intersection_points


def create_polygons(num_sectors: int):
    """
    Creates polygons for each sector formed by the radius lines and the square's boundary.

    Parameters
    ----------
    num_sectors : int
        Number of sectors to divide the circle into.

    Returns
    -------
    list of list of tuples
        Each polygon is represented as a list of (x, y) tuples.
    """
    center = (0.5, 0.5)
    points = find_intersection_points_centered(num_sectors)

    polygons = []
    square_apexes = [(0, 0), (1, 0), (1, 1), (0, 1)]

    for i in range(num_sectors):
        # Define the current and next intersection points
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]

        # Initialize the polygon with the center and intersection points
        if num_sectors != 2:
            polygon = [center, p1]
        else:
            polygon = [p1]

        # Special case for 2 sectors: Add the square apex again to form a triangle
        if num_sectors == 2:
            if i == 0:
                polygon.append(square_apexes[3])
            elif i == 1:
                polygon.append(square_apexes[1])

        # Special case for 3 sectors: Add the square apex again to form a pentagon
        elif num_sectors == 3 and i == 0:
            polygon.append(square_apexes[3])
            polygon.append(square_apexes[2])

        # Special case for 4 sectors: No need to add the square apexes as they are already included
        elif num_sectors == 4:
            pass

        else:
            # Add intermediate square apexes if necessary
            for apex in square_apexes:
                if min(p1[0], p2[0]) <= apex[0] <= max(p1[0], p2[0]) and min(
                    p1[1], p2[1]
                ) <= apex[1] <= max(p1[1], p2[1]):
                    polygon.append(apex)

        # Add the second intersection point and close the polygon
        polygon.append(p2)

        # Append the polygon to the list
        polygons.append(polygon)

    return polygons


def extract_polygon_coordinates(polygons):
    """
    Extracts x and y coordinates from a list of polygons, rounded to 2 decimal places.

    Parameters
    ----------
    polygons : list of list of tuples
        Each polygon is represented as a list of (x, y) tuples.

    Returns
    -------
    tuple of lists
        xpts_list : list of lists of floats
            x-coordinates of the polygons, rounded to 2 decimal places.
        ypts_list : list of lists of floats
            y-coordinates of the polygons, rounded to 2 decimal places.
    """
    xpts_list = []
    ypts_list = []

    for polygon in polygons:
        xpts = [round(float(point[0]), 2) for point in polygon]
        ypts = [round(float(point[1]), 2) for point in polygon]
        xpts_list.append(xpts)
        ypts_list.append(ypts)

    return xpts_list, ypts_list


def get_x_y_points(num_sectors: int):
    """
    Returns the x and y coordinates of the polygons formed by radius partitions.

    Parameters
    ----------
    num_sectors : int
        The number of sectors to divide the circle into.

    Returns
    -------
    tuple of lists
        xpts_list : list of lists of floats
            x-coordinates of the polygons, rounded to 2 decimal places.
        ypts_list : list of lists of floats
            y-coordinates of the polygons, rounded to 2 decimal places.
    """
    if num_sectors == 1:
        xpts = [0, 0, 1, 1]
        ypts = [1, 0, 0, 1]
        return ([xpts], [ypts])

    # Create polygons
    polygons = create_polygons(num_sectors)
    xpts_list, ypts_list = extract_polygon_coordinates(polygons)
    return (xpts_list, ypts_list)


def get_positions(num_sectors: int):
    """
    Returns the positions of the polygons formed by radius partitions.

    Parameters
    ----------
    num_sectors : int
    The number of sectors to divide the circle into.

    Returns
    -------
    list
        Positions of the polygons.
    """
    positions = None

    if num_sectors == 4:
        positions = ["top", "right", "bottom", "left"]
    elif num_sectors == 3:
        positions = ["top", "lower-left", "lower-right"]
    elif num_sectors == 2:
        positions = ["upper", "lower"]
    elif num_sectors == 1:
        positions = ["box"]

    return positions


def get_glyph_row_points(glyph_rows: int):

    xpts = [0, 0, 1, 1]
    xpts_list = [xpts] * glyph_rows
    row_height = 1/glyph_rows
    ypts_list = []
    positions = []
    for g in range(0, glyph_rows):
        gypts = np.arange(0, 1+row_height, row_height).astype('float')
        gypts = np.round(gypts, 3)
        gypts_list = [float(x) for x in gypts]
        g_array = [gypts_list[g], gypts_list[g+1], gypts_list[g+1], gypts_list[g]]
        ypts_list.append(g_array)
        position = f'region{g+1}'
        positions.append(position)

    return xpts_list, ypts_list, positions
