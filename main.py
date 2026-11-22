#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261122 entry (v6).

The repository holds the finished front page as entry.png, drawn at build
time by draw.py. The grading container runs Python 3.13 with the standard
library only and no network, so this program simply copies the committed
image to the output directory, byte for byte, which keeps the two grading
runs identical.
"""

import os


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as fh:
        data = fh.read()
    with open(dst, "wb") as fh:
        fh.write(data)
    assert os.path.getsize(dst) == len(data), "copied image is truncated"
    print("wrote", dst, len(data), "bytes")


if __name__ == "__main__":
    main()
