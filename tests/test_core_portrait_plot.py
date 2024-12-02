import unittest

import numpy as np
from bokeh.plotting import Figure

from ESMBenchmarkViz import portrait_plot


class TestPortraitPlot(unittest.TestCase):
    def test_minimal_valid_input(self):
        data = np.array([[1, 2], [3, 4]])
        xaxis_labels = ["A", "B"]
        yaxis_labels = ["C", "D"]
        plot = portrait_plot(data, xaxis_labels, yaxis_labels, show_plot=False)
        self.assertIsInstance(plot, Figure)

    def test_3d_data_input(self):
        data = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
        xaxis_labels = ["A", "B"]
        yaxis_labels = ["C", "D"]
        plot = portrait_plot(data, xaxis_labels, yaxis_labels, show_plot=False)
        self.assertIsInstance(plot, Figure)

    def test_with_annotations(self):
        data = np.array([[1, 2], [3, 4]])
        annotate_data = np.array([[0.1, 0.2], [0.3, 0.4]])
        xaxis_labels = ["A", "B"]
        yaxis_labels = ["C", "D"]
        plot = portrait_plot(
            data,
            xaxis_labels,
            yaxis_labels,
            annotate=True,
            annotate_data=annotate_data,
            show_plot=False,
        )
        self.assertIsInstance(plot, Figure)

    def test_clickable_urls(self):
        data = np.array([[1, 2], [3, 4]])
        xaxis_labels = ["A", "B"]
        yaxis_labels = ["C", "D"]
        img_url = ["http://example.com/img1", "http://example.com/img2"]
        plot = portrait_plot(
            data,
            xaxis_labels,
            yaxis_labels,
            clickable=True,
            img_url=img_url,
            show_plot=False,
        )
        self.assertIsInstance(plot, Figure)

    def test_custom_color_map_bounds(self):
        data = np.array([[1, 2], [3, 4]])
        xaxis_labels = ["A", "B"]
        yaxis_labels = ["C", "D"]
        cmap_bounds = [0, 2, 4]
        plot = portrait_plot(
            data, xaxis_labels, yaxis_labels, cmap_bounds=cmap_bounds, show_plot=False
        )
        self.assertIsInstance(plot, Figure)


if __name__ == "__main__":
    unittest.main()
