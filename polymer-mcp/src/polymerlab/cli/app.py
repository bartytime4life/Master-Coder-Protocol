"""Minimal Typer CLI for polymerlab used in tests."""
from __future__ import annotations

import os
from pathlib import Path
from typing import List

import pandas as pd
import typer

from polymerlab.io.loader import glob_files
from polymerlab.io.schema import build_validator, iter_records
from polymerlab.featurize.basic import to_dataframe

app = typer.Typer()


@app.command("version")
def version() -> None:
    from polymerlab import __version__
    typer.echo(__version__)


@app.command("data-validate")
def data_validate(
    in_paths: List[str] = typer.Option(..., "--in", help="Input JSON/YAML files (glob patterns OK)."),
    schema_path: str = typer.Option("conf/schema/mcp_polymers.schema.yaml", "--schema", help="JSON Schema (YAML)."),
) -> None:
    paths = glob_files(in_paths)
    if not paths:
        raise typer.Exit(code=2)
    validator = build_validator(schema_path)
    errors = []
    for path, rec in iter_records(paths):
        errors.extend([e for e in validator.iter_errors(rec)])
    if errors:
        for e in errors:
            loc = "/".join(map(str, e.path)) or "<root>"
            typer.echo(f"{e.instance}: {loc}: {e.message}")
        raise typer.Exit(code=1)
    typer.echo(f"Validated {len(paths)} file(s).")


@app.command("data-featurize")
def data_featurize(
    in_dir: str = typer.Option("data/raw", "--in", help="Directory of raw/interim JSON/YAML files."),
    out_dir: str = typer.Option("data/processed", "--out", help="Directory for processed outputs."),
    schema_path: str = typer.Option("conf/schema/mcp_polymers.schema.yaml", "--schema", help="Schema for validation."),
) -> None:
    os.makedirs(out_dir, exist_ok=True)
    paths = glob_files([str(Path(in_dir) / "*.json"), str(Path(in_dir) / "*.yml"), str(Path(in_dir) / "*.yaml")])
    validator = build_validator(schema_path)
    recs = []
    for p, rec in iter_records(paths):
        if list(validator.iter_errors(rec)):
            continue
        recs.append((p, rec))
    df = to_dataframe(recs)
    out_csv = str(Path(out_dir) / "features.csv")
    df.to_csv(out_csv, index=False)
    typer.echo(out_csv)

if __name__ == "__main__":
    app()

