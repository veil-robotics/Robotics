from __future__ import annotations

import typer

from .anonymize import app as anonymize_app

app = typer.Typer(add_completion=False)
app.add_typer(anonymize_app, name="anonymize")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
