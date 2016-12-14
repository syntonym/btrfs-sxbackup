from btrfs_sxbackup.cli import parser
import argparse
import os.path

def get_subparsers(parser):
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            yield action

template = """
{prog_name}-{command}
{prog_name_length}={command_length}

Synopsis
--------

.. autoprogram:: btrfs_sxbackup.cli:parser
    :maxdepth: 1
    :start_command: {command}
    :prog: {prog_name}

See also
--------

:manpage:`{prog_name}(1)`
"""

def make_rts(prog_name, command, directory):
    with open(os.path.join(directory, command+".rst"), mode="w") as f:
        f.write(template.format(command=command,
            command_length=len(command)*"=",
            prog_name=prog_name.replace("_", "-"),
            prog_name_length=len(prog_name)*"="))
    

def make_rsts(parser, prog_name):
    for subparser in get_subparsers(parser):
        for choice in subparser.choices:
            make_rts(str(prog_name), choice, "./docs/man_pages")


import btrfs_sxbackup.cli

make_rsts(btrfs_sxbackup.cli.parser, "btrfs_sxbackup")
