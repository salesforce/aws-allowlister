#! /usr/bin/env python
import click
from aws_allowlister import command
from aws_allowlister.bin.version import __version__


@click.group()
@click.version_option(version=__version__)
def aws_allowlister():
    """
    Easily generate AWS AllowList SCPs according to compliance requirements.
    """


aws_allowlister.add_command(command.generate.generate)
aws_allowlister.add_command(command.rebuild.rebuild)


def main():
    """Easily generate AWS AllowList SCPs according to compliance requirements."""
    aws_allowlister()


if __name__ == "__main__":
    main()
