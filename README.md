# Circler

A rainbow spiral of growing, rotating 3D tetrahedra. Pygame handles the window
and events; ModernGL renders the lit faces with depth testing and, where
available, 4× multisample antialiasing.

Requires Python 3.13+ and an OpenGL 3.3 capable graphics driver.

```sh
uv sync
uv run circler.py
```

Resize the window to change the canvas size. Press Escape or close the window
to quit. Spawn timing and rainbow cycling can be adjusted with the constants
at the top of `circler.py`.
