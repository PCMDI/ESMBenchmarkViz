import unittest

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure

from ESMBenchmarkViz.core_scatter_plot import scatter_plot


class TestScatterPlot(unittest.TestCase):
    def setUp(self):
        self.x = [1, 2, 3]
        self.y = [6, 7, 2]
        self.names = ["Point A", "Point B", "Point C"]
        self.images = [
            "images/image1.jpg",
            None,
            "images/image3.jpg",
        ]

    def test_scatter_plot_no_images(self):
        plot = scatter_plot(self.x, self.y, self.names, images=None, show_plot=False)
        self.assertIsInstance(plot, figure)
        self.assertEqual(len(plot.renderers), 1)
        self.assertEqual(plot.title.text, "Interactive Scatter Plot")

    def test_scatter_plot_with_images(self):
        layout = scatter_plot(
            self.x, self.y, self.names, images=self.images, show_plot=False
        )
        self.assertEqual(len(layout.children), 2)
        plot = layout.children[0]
        controls = layout.children[1]
        self.assertIsInstance(plot, figure)
        self.assertEqual(len(plot.renderers), 1)
        self.assertEqual(plot.title.text, "Interactive Scatter Plot")
        self.assertEqual(len(controls.children), 3)

    def test_data_source(self):
        plot = scatter_plot(self.x, self.y, self.names, images=None, show_plot=False)
        source = plot.renderers[0].data_source
        self.assertIsInstance(source, ColumnDataSource)
        self.assertEqual(len(source.data["x"]), 3)
        self.assertEqual(len(source.data["y"]), 3)
        self.assertEqual(len(source.data["names"]), 3)

    def test_invalid_input_length(self):
        with self.assertRaises(ValueError):
            scatter_plot(self.x, self.y, self.names[:2], images=None, show_plot=False)

    def test_invalid_image_length(self):
        with self.assertRaises(ValueError):
            scatter_plot(
                self.x, self.y, self.names, images=self.images[:2], show_plot=False
            )


if __name__ == "__main__":
    unittest.main()
