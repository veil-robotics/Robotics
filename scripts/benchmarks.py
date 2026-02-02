from __future__ import annotations

import argparse
import time
from pathlib import Path

from src.core.modes import parse_mode
from src.core.pipeline import anonymize_video


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--mode", type=str, default="blur")
    args = parser.parse_args()

    start = time.time()
    anonymize_video(args.input, args.output, args.summary, parse_mode(args.mode))
    elapsed = time.time() - start
    print(f"Elapsed: {elapsed:.2f}s")


if __name__ == "__main__":
    main()
