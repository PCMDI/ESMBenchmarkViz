"""
Convert MOV to GIF and adjust GIF speed using Python.

This script demonstrates how to convert a MOV video file to an animated GIF, which is useful for sharing
videos (e.g., demonstration of interactive plots) on platforms that do not support video uploads.
It also shows how to adjust the speed of an animated GIF.

Proceed `pip install moviepy` and `pip install PIL` before running this script if needed.

History
-------
2024-11-10: Initial version, Jiwoo Lee
"""

import os

from moviepy.editor import VideoFileClip
from PIL import Image, ImageSequence


def main():
    # User settings
    input_mov_path = "example_taylor_diagram.mov"
    output_gif_path = "example_taylor_diagram.gif"

    # Convert MOV to GIF (Do not change below this line) -----------------------
    interim_gif_path = "output_interim.gif"

    mov_to_gif(input_mov_path, interim_gif_path, fps=10)
    adjust_gif_speed(
        interim_gif_path, output_gif_path, speed_factor=2
    )  # adjust speed by 2x

    # Remove interim GIF
    os.remove(interim_gif_path)


def mov_to_gif(input_mov_path: str, output_gif_path: str, fps: int = 10):
    """
    Converts a .mov video file to an animated GIF.

    Parameters
    ----------
    input_mov_path : str
        Path to the input .mov file.
    output_gif_path : str
        Path where the output GIF file will be saved.
    fps : int, optional
        Frames per second for the GIF. Lowering the FPS can reduce the file size, by default 10.

    Example
    -------
    >>> mov_to_gif("input.mov", "output.gif", fps=10)

    """
    # Load the video clip
    clip = VideoFileClip(input_mov_path)

    # Convert to GIF
    clip.write_gif(output_gif_path, fps=fps)

    print(f"GIF saved at: {output_gif_path}")


def adjust_gif_speed(
    input_gif_path, output_gif_path, speed_factor, default_duration=100
):
    """
    Adjust the speed of an animated GIF.

    Parameters
    ----------
    input_gif_path : str
        Path to the input GIF file.
    output_gif_path : str
        Path to save the output GIF file with adjusted speed.
    speed_factor : float
        Factor to adjust the speed. A value greater than 1 speeds up the GIF,
        while a value less than 1 slows it down.
    default_duration : int, optional
        Default duration (in ms) per frame if 'duration' metadata is missing, by default 100 ms.

    Example
    -------
    Adjusting the speed of a GIF:

    >>> input_gif = "input.gif"
    >>> output_gif = "output_adjusted_speed.gif"
    >>> speed_factor = 2  # Use 2 for double speed, 0.5 for half speed
    >>> adjust_gif_speed(input_gif, output_gif, speed_factor)
    """
    with Image.open(input_gif_path) as img:
        frames = []
        durations = []

        for frame in ImageSequence.Iterator(img):
            frames.append(frame.copy())
            # Use the default duration if 'duration' is missing
            frame_duration = frame.info.get("duration", default_duration)
            durations.append(int(frame_duration / speed_factor))

        # Save adjusted GIF
        frames[0].save(
            output_gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=img.info.get("loop", 0),
        )


if __name__ == "__main__":
    main()
