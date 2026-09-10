#!/usr/bin/env python
"""
Generate thumbnail images for documentation gallery.

This script creates PNG thumbnails for scatter_plot and portrait_plot
to be used in the documentation gallery.
"""

import sys
from pathlib import Path

# Add package to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import numpy as np
from bokeh.io import export_png

from ESMBenchmarkViz import scatter_plot, portrait_plot


def create_scatter_plot_thumbnail():
    """Create thumbnail for scatter_plot."""
    print("Creating scatter_plot thumbnail...")

    # Sample data similar to the example
    x = [1.26, 0.93, 0.83, 1.15, 0.78, 1.42]
    y = [0.87, 0.91, 0.93, 0.85, 0.94, 0.82]
    names = ["ACCESS-CM2", "E3SM-1-0", "GFDL-CM4", "IPSL-CM6A", "MRI-ESM2", "UKESM1"]

    # Create plot
    p = scatter_plot(
        x, y, names,
        title="Model Performance: RMSE vs Correlation",
        width=600,
        height=400,
        show_plot=False
    )

    # Export as PNG
    output_path = Path(__file__).parent / "interactive_scatter_plot.png"
    try:
        export_png(p, filename=str(output_path))
        print(f"✓ Saved: {output_path}")
        return output_path
    except Exception as e:
        print(f"✗ Failed to export: {e}")
        print("  Tip: Install selenium and browser driver for PNG export")
        return None


def create_portrait_plot_thumbnail():
    """Create thumbnail for portrait_plot."""
    print("\nCreating portrait_plot thumbnail...")

    # Sample data similar to the example
    data = np.random.randn(8, 7)

    xaxis_labels = ['Temperature', 'Precipitation', 'Wind', 'Humidity', 'Pressure', 'Radiation', 'Cloud']
    yaxis_labels = ['ACCESS-CM2', 'E3SM-1-0', 'GFDL-CM4', 'IPSL-CM6A', 'MRI-ESM2', 'NorESM2', 'UKESM1', 'CanESM5']

    # Create plot
    p = portrait_plot(
        data,
        xaxis_labels=xaxis_labels,
        yaxis_labels=yaxis_labels,
        width=600,
        height=500,
        show_plot=False
    )

    # Export as PNG
    output_path = Path(__file__).parent / "interactive_portrait_plot.png"
    try:
        export_png(p, filename=str(output_path))
        print(f"✓ Saved: {output_path}")
        return output_path
    except Exception as e:
        print(f"✗ Failed to export: {e}")
        print("  Tip: Install selenium and browser driver for PNG export")
        return None


def update_conf_py(scatter_path, portrait_path):
    """Update conf.py with new thumbnail paths."""
    print("\nUpdating conf.py...")

    conf_path = Path(__file__).parent.parent / "conf.py"

    with open(conf_path, 'r') as f:
        content = f.read()

    # Find and update nbsphinx_thumbnails
    old_config = 'nbsphinx_thumbnails = {\n    "examples/example_taylor_diagram": "_static/example_taylor_diagram.gif"\n}'

    new_config = '''nbsphinx_thumbnails = {
    "examples/example_taylor_diagram": "_static/example_taylor_diagram.gif",
    "examples/example_scatter_plot": "_static/interactive_scatter_plot.png",
    "examples/example_portrait_plot": "_static/interactive_portrait_plot.png"
}'''

    if old_config in content:
        content = content.replace(old_config, new_config)

        with open(conf_path, 'w') as f:
            f.write(content)

        print(f"✓ Updated: {conf_path}")
        return True
    else:
        print(f"⚠ Could not find expected config in {conf_path}")
        print("  You may need to update manually:")
        print(new_config)
        return False


def main():
    """Main function."""
    print("="*70)
    print("Creating Documentation Thumbnails")
    print("="*70)

    scatter_path = create_scatter_plot_thumbnail()
    portrait_path = create_portrait_plot_thumbnail()

    if scatter_path and portrait_path:
        print("\n" + "="*70)
        print("SUCCESS!")
        print("="*70)
        update_conf_py(scatter_path, portrait_path)

        print("\nThumbnails created:")
        print(f"  - {scatter_path}")
        print(f"  - {portrait_path}")
        print("\nNext steps:")
        print("  1. Rebuild documentation: cd docs && make html")
        print("  2. Check gallery: open docs/_build/html/gallery.html")
        return True
    else:
        print("\n" + "="*70)
        print("PARTIAL FAILURE")
        print("="*70)
        print("Some thumbnails could not be created.")
        print("You may need to:")
        print("  1. Install selenium: pip install selenium")
        print("  2. Install browser driver:")
        print("     - conda install -c conda-forge firefox geckodriver")
        print("     - OR pip install chromedriver-binary")
        print("  3. Try again: python create_thumbnails.py")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
