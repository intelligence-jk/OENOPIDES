# manim-board-kit

Lay out a step-by-step maths board and generate a ready-to-render Manim scene from it.

## What it solves
Writing a Manim scene for a worked solution means choosing a y position for every line so nothing runs off the bottom of the frame. This does it for you: give it a title and the lines of working, and it prints a scene file where the lines are evenly spaced and always inside the frame. The kit itself is pure Python 3.10+ with no dependencies; to render the scene you install [Manim Community](https://www.manim.community/) separately.

## Example
```bash
python -m boardkit "Solve 2x + 3 = 11" "2x + 3 = 11" "2x = 8" "x = 4" > scene.py
manim -pql scene.py Board
```
`scene.py`:
```python
from manim import *


class Board(Scene):
    def construct(self):
        title = Text('Solve 2x + 3 = 11', font_size=40).move_to(UP * 3.5)
        self.play(Write(title))
        step1 = MathTex('2x + 3 = 11').move_to(UP * 2.7)
        self.play(Write(step1))
        self.wait(0.5)
        step2 = MathTex('2x = 8').move_to(UP * 1.9)
        self.play(Write(step2))
        self.wait(0.5)
        step3 = MathTex('x = 4').move_to(UP * 1.1)
        self.play(Write(step3))
        self.wait(0.5)
        self.wait(1)
```
Lines are written as LaTeX (`\frac{1}{2}` and so on), because they go to `MathTex`.

## The maths behind it
Manim's default frame is 8 units high, so y runs from +4 to -4. The first line sits at y = 3.5 and the last line may not go below y = -3.5. For `n` lines the gap between neighbours is `g = min(0.8, 7 / (n - 1))`, and line `i` (from 0) sits at `3.5 - i g`. A short board keeps the comfortable 0.8 gap; a long one is squeezed so the last line lands exactly on -3.5. For 12 lines the gap is `7/11` and the last line is at `3.5 - 11 x 7/11 = -3.5`. Positions are exact `Fraction` values and are converted to decimals only when the file is written.

## Install and run
```bash
python -m pip install -e .
python -m boardkit "Title" "line 1" "line 2"
python -m pytest
```

## Licence
MIT. Made by Math & Myth (mathandmyth.ae): one to one maths mentoring, online, across the UAE.
