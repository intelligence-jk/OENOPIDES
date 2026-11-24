import ast
from fractions import Fraction as F

import pytest

from boardkit import FRAME_BOTTOM, FRAME_TOP, generate_scene, layout
from boardkit.__main__ import main


def test_layout_short_board_uses_max_gap():
    assert layout(3) == [F(7, 2), F(7, 2) - F(4, 5), F(7, 2) - F(8, 5)]


def test_layout_long_board_squeezed_to_fit():
    ys = layout(12)
    assert ys[0] == FRAME_TOP and ys[-1] == FRAME_BOTTOM
    gaps = {a - b for a, b in zip(ys, ys[1:])}
    assert len(gaps) == 1 and gaps.pop() == F(7, 11)


@pytest.mark.parametrize("n", range(1, 40))
def test_layout_always_inside_frame_and_ordered(n):
    ys = layout(n)
    assert len(ys) == n
    assert all(FRAME_BOTTOM <= y <= FRAME_TOP for y in ys)
    assert ys == sorted(ys, reverse=True)


def test_layout_errors():
    with pytest.raises(ValueError):
        layout(0)
    with pytest.raises(ValueError):
        layout(3, top=F(0), bottom=F(1))


def test_scene_is_valid_python_with_one_play_per_line():
    src = generate_scene("Solve 2x + 3 = 11", ["2x + 3 = 11", "2x = 8", "x = 4"])
    tree = ast.parse(src)
    cls = [n for n in tree.body if isinstance(n, ast.ClassDef)][0]
    assert cls.name == "Board"
    assert src.count("self.play(Write(") == 4  # title + 3 steps
    assert "MathTex('x = 4')" in src


def test_quotes_and_backslashes_survive():
    src = generate_scene("It's \"quoted\"", [r"\frac{1}{2} + \frac{1}{3} = \frac{5}{6}"])
    ast.parse(src)
    assert r"\\frac{1}{2}" in src


def test_scene_errors():
    with pytest.raises(ValueError):
        generate_scene("t", [])
    with pytest.raises(ValueError):
        generate_scene("t", ["x"], class_name="not valid")


def test_cli(capsys):
    assert main(["Title", "x = 1"]) == 0
    ast.parse(capsys.readouterr().out)
    assert main(["only title"]) == 2
