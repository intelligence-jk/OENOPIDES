"""python -m boardkit "Title" "step 1" "step 2" ... > scene.py   then: manim -pql scene.py Board"""
import sys

from .core import generate_scene


def main(argv=None) -> int:
    a = sys.argv[1:] if argv is None else argv
    if len(a) < 2:
        print('usage: python -m boardkit "TITLE" "STEP" ["STEP" ...]', file=sys.stderr)
        return 2
    sys.stdout.write(generate_scene(a[0], a[1:]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
