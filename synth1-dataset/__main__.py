from pathlib import Path

import click

from .generate_csv import generate_csv
from .generate_sounds import collect_wav


@click.command()
@click.argument("command")
@click.argument("in_path")
@click.argument("out_path")
@click.option(
    "--start",
    help="Start collectiong wavs at index (only for the wav command)",
    default=0,
)
def main_cli(command: str, in_path: str, out_path: str, start: int):
    print(start + 1)
    if command == "csv":
        generate_csv(Path(in_path), Path(out_path))
    elif command == "wav":
        collect_wav(Path(in_path), Path(out_path), start=start)
    else:
        print("Nothing to do.")


if __name__ == "__main__":
    main_cli()
