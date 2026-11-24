"""Lay out a step-by-step board and write a Manim scene for it.

The scene file this produces needs Manim Community to run; this package itself
needs nothing. Layout uses exact Fraction arithmetic, in Manim scene units
(the default frame is 8 units high, so y runs from +4 to -4).
"""
from __future__ import annotations

from fractions import Fraction as F

FRAME_TOP = F(7, 2)  # first line sits here (3.5), inside the 4.0 frame edge
FRAME_BOTTOM = F(-7, 2)  # last line may not go below this
MAX_GAP = F(4, 5)  # never space lines wider than 0.8 units


def layout(n_lines: int, top: F = FRAME_TOP, bottom: F = FRAME_BOTTOM, max_gap: F = MAX_GAP) -> list[F]:
    """y position for each of n_lines lines: evenly spaced, gap at most max_gap, inside [bottom, top]."""
    if n_lines < 1:
        raise ValueError("need at least one line")
    if top <= bottom:
        raise ValueError("top must be above bottom")
    if n_lines == 1:
        return [top]
    gap = min(max_gap, (top - bottom) / (n_lines - 1))
    return [top - i * gap for i in range(n_lines)]


def _py_str(s: str) -> str:
    return repr(s)


def generate_scene(title: str, steps: list[str], class_name: str = "Board") -> str:
    """Python source for a Manim Scene that writes the title, then each step line by line."""
    if not class_name.isidentifier():
        raise ValueError("class_name must be a valid Python name")
    if not steps:
        raise ValueError("need at least one step")
    ys = layout(len(steps) + 1)  # first slot is the title
    lines = [
        "from manim import *",
        "",
        "",
        f"class {class_name}(Scene):",
        "    def construct(self):",
        f"        title = Text({_py_str(title)}, font_size=40).move_to(UP * {float(ys[0])})",
        "        self.play(Write(title))",
    ]
    for i, (s, y) in enumerate(zip(steps, ys[1:]), 1):
        lines += [
            f"        step{i} = MathTex({_py_str(s)}).move_to(UP * {float(y)})",
            f"        self.play(Write(step{i}))",
            "        self.wait(0.5)",
        ]
    lines.append("        self.wait(1)")
    return "\n".join(lines) + "\n"
