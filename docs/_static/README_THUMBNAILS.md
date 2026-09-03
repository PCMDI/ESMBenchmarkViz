# Creating Thumbnails for Documentation Gallery

The documentation gallery requires thumbnail images for each example notebook.

## Current Status

- ✅ `example_taylor_diagram.gif` - Exists (6.5 MB animated GIF)
- ⚠️ `interactive_scatter_plot.png` - **Needs to be created**
- ⚠️ `interactive_portrait_plot.png` - **Needs to be created**

## Configuration

Thumbnails are configured in `docs/conf.py`:

```python
nbsphinx_thumbnails = {
    "examples/example_taylor_diagram": "_static/example_taylor_diagram.gif",
    "examples/example_scatter_plot": "_static/interactive_scatter_plot.png",
    "examples/example_portrait_plot": "_static/interactive_portrait_plot.png"
}
```

## Method 1: Automated (Requires selenium)

### Prerequisites

```bash
conda activate ESMBenchmarkViz_20260318
pip install selenium pillow
conda install -c conda-forge firefox geckodriver
# OR
pip install chromedriver-binary
```

### Run Script

```bash
cd docs/_static
python create_thumbnails.py
```

This will:
1. Create `interactive_scatter_plot.png` (600×400)
2. Create `interactive_portrait_plot.png` (600×500)
3. Update `conf.py` (already done)

---

## Method 2: Manual Screenshot (Always Works)

### For Scatter Plot

1. **Open HTML file**:
   ```bash
   open docs/examples/interactive_scatter_plot.html
   ```

2. **Take screenshot**:
   - Mac: Cmd+Shift+4, then Space, click window
   - Windows: Win+Shift+S
   - Or use browser: Right-click → "Capture screenshot"

3. **Save as**:
   ```
   docs/_static/interactive_scatter_plot.png
   ```

4. **Recommended size**: 600×400 pixels

### For Portrait Plot

1. **Open HTML file**:
   ```bash
   open docs/examples/interactive_portrait_plot.html
   ```

2. **Take screenshot** (same as above)

3. **Save as**:
   ```
   docs/_static/interactive_portrait_plot.png
   ```

4. **Recommended size**: 600×500 pixels

---

## Method 3: From Jupyter Notebook

If you have the notebooks running in Jupyter:

1. **Run the notebook**:
   - Open `example_scatter_plot.ipynb` or `example_portrait_plot.ipynb`
   - Run all cells

2. **Screenshot the plot**:
   - Take a screenshot of the rendered Bokeh plot
   - Crop to just the plot area

3. **Save**:
   - Save to `docs/_static/` with the appropriate name
   - Optimize size if needed (600px wide is good)

---

## Method 4: Use Existing Images

If you have existing PNG exports from the notebooks:

```bash
# Copy from examples directory if they exist
cp docs/examples/scatter_plot_example.png docs/_static/interactive_scatter_plot.png
cp docs/examples/portrait_plot_example.png docs/_static/interactive_portrait_plot.png
```

---

## Optimization (Optional)

If thumbnails are too large:

```bash
# Using ImageMagick
convert interactive_scatter_plot.png -resize 600x400 -quality 85 interactive_scatter_plot.png
convert interactive_portrait_plot.png -resize 600x500 -quality 85 interactive_portrait_plot.png

# OR use online tools:
# https://tinypng.com/
# https://www.iloveimg.com/compress-image
```

---

## Verify

After creating thumbnails:

1. **Check files exist**:
   ```bash
   ls -lh docs/_static/interactive_*.png
   ```

2. **Rebuild documentation**:
   ```bash
   cd docs
   make clean
   make html
   ```

3. **View gallery**:
   ```bash
   open _build/html/gallery.html
   ```

4. **Look for thumbnails** in the gallery grid

---

## Troubleshooting

### Thumbnails not showing in gallery

- Check file paths in `conf.py` match actual files
- Ensure filenames are exact (case-sensitive)
- Rebuild docs with `make clean && make html`
- Check browser console for 404 errors

### Images too large

- Thumbnails should be < 1 MB each
- Target resolution: ~600px wide
- Use PNG format for best quality at small size

### Can't export PNG from Bokeh

- Use manual screenshot method instead
- Or install selenium + browser driver
- Or use the animated GIF creation scripts (see `README_GIF_CREATION.md`)

---

## Quick Reference

**Automated**: `python create_thumbnails.py`  
**Manual**: Screenshot HTML → Save to `_static/`  
**Verify**: `ls _static/interactive_*.png`  
**Build**: `cd docs && make html`  
**Check**: `open _build/html/gallery.html`
