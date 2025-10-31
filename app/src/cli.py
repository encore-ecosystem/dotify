from argparse import ArgumentParser
from dotify_app import command

from pathlib import Path


def main():
    parser = ArgumentParser(
        prog="dotify", description="Dotify - a modular configuration tool"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- dotify init ---
    parser_init = subparsers.add_parser("init", help="Initialize a new project")
    parser_init.set_defaults(func=command.init)

    # --- dotify apply ---
    parser_apply = subparsers.add_parser("apply", help="Apply configuration")
    parser_apply.add_argument(
        "-m",
        "--manifest",
        type=Path,
        default=Path("./manifests"),
        help="Path to manifests directory (default: ./manifests)",
    )
    parser_apply.set_defaults(func=command.apply)

    # Parse and dispatch
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    entrypoint()
