from btrfs_sxbackup.cli import parser
import argparse
import os.path

import jinja2

def get_subparsers(parser):
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            yield action

template = """
:orphan:

{{ prog_name.replace("_", "-") }}{% if command %}-{{command}}{% endif %}
{{ "="*len(prog_name)}}={{"="*len(command)}}

Synopsis
--------

.. autoprogram:: btrfs_sxbackup.cli:parser
    :maxdepth: 1
    :prog: {{ prog_name }}
    {% if command -%}
    :start_command: {{ command }}
    {%- endif %}

{% if description -%}
Description
-----------

{{ description }}
{%- endif -%}

{%- if see_also -%}
See also
--------

{% for page in see_also -%}
:manpage:`{{ page.replace("_", "-") }}(1)`
{% endfor %}
{%- endif -%}
"""

main_template = """
Manpages
========

.. toctree:: 

    {% for page in pages -%}
    {{ page }}
    {% endfor %}
"""

def make_rts(name, prog_name, command, description, see_also, directory, j2_template):
    with open(os.path.join(directory, name+".rst"), mode="w") as f:
        f.write(j2_template.render(prog_name=prog_name,
            command=command,
            description=description,
            see_also=see_also,
            len=len))

def make_rsts(parser, prog_name):
    subpages = []
    j2_template = jinja2.Template(template)
    for subparser in get_subparsers(parser):
        for choice in subparser.choices:
            subpages.append(choice)
            make_rts(choice, str(prog_name), choice, "", [str(prog_name)], "./docs/man_pages", j2_template)

    see_also = [str(prog_name).replace("_", "-") + "-" + page for page in subpages]
    make_rts(str(prog_name), str(prog_name), "", "", see_also, "./docs/man_pages", j2_template)

    pages = ["man_pages/" + page for page in subpages] + ["man_pages/" + str(prog_name)]

    with open(os.path.join("./docs/", "manpages.rst"), mode="w") as f:
        f.write(jinja2.Template(main_template).render(pages=pages))


import btrfs_sxbackup.cli

make_rsts(btrfs_sxbackup.cli.parser, "btrfs_sxbackup")
