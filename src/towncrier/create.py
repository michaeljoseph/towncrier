# Copyright (c) Stephen Finucane, 2019
# See LICENSE for details.

"""
Create a new fragment.
"""

from __future__ import absolute_import

import os
import click

from ._settings import load_config


@click.command(name="create")
@click.option("--dir", "directory", default=".")
@click.argument("filename")
def _main(directory, filename):
    return __main(directory, filename)


def __main(directory, filename):
    """
    The main entry point.
    """
    directory = os.path.abspath(directory)
    config = load_config(directory)

    definitions = config["types"] or []
    if len(filename.split(".")) < 2 or (
        filename.split(".")[-1] not in definitions
        and filename.split(".")[-2] not in definitions
    ):
        raise click.BadParameter(
            "Expected filename '{}' to be of format '{{name}}.{{type}}', "
            "where '{{name}}' is an arbitrary slug and '{{type}}' is "
            "one of: {}".format(filename, ", ".join(definitions))
        )

    if config.get("directory"):
        fragments_directory = os.path.abspath(config["directory"])
    else:
        fragments_directory = os.path.abspath(
            os.path.join(
                directory, config["package_dir"], config["package"], "newsfragments"
            )
        )

    if not os.path.exists(fragments_directory):
        os.makedirs(fragments_directory)

    segment_file = os.path.join(fragments_directory, filename)
    if os.path.exists(segment_file):
        raise click.ClickException("{} already exists".format(segment_file))

    with open(segment_file, "w") as f:
        f.writelines(["Add your info here"])

    click.echo("Created news fragment at {}".format(segment_file))


if __name__ == "__main__":  # pragma: no cover
    _main()
