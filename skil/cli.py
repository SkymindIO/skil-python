#!/usr/bin python
# -*- coding: utf-8 -*-
################################################################################
# Copyright (c) 2015-2018 Skymind, Inc.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0
################################################################################

import argparse
import json
import os
import sys
import pkg_resources
import argcomplete
import traceback
import subprocess
from builtins import input

import click
from click.exceptions import ClickException
from dateutil import parser


class CLI(object):

    def __init__(self):
        self.var_args = None
        self.command = None

    def command_dispatcher(self, args=None):
        desc = ('pydl4j,  a system to manage your DL4J dependencies from Python.\n')
        parser = argparse.ArgumentParser(description=desc)
        parser.add_argument(
            '-v', '--version', action='version',
            version=pkg_resources.get_distribution("pydl4j").version,
            help='Print pydl4j version'
        )

        subparsers = parser.add_subparsers(title='subcommands', dest='command')
        subparsers.add_parser('init', help='Initialize pydl4j')
        subparsers.add_parser('install', help='Install jars for pydl4j')

        argcomplete.autocomplete(parser)
        args = parser.parse_args(args)
        self.var_args = vars(args)

        if not args.command:
            parser.print_help()
            return

        self.command = args.command

        if self.command == 'init':
            self.init()
            return

    def init(self):

        click.echo(click.style(u"""\n███████╗██╗  ██╗██╗██╗     
██╔════╝██║ ██╔╝██║██║     
███████╗█████╔╝ ██║██║     
╚════██║██╔═██╗ ██║██║     
███████║██║  ██╗██║███████╗
╚══════╝╚═╝  ╚═╝╚═╝╚══════╝\n""", fg='blue', bold=True))

        click.echo(click.style("SKIL", bold=True) +
                   " deploy your models to production from Python!\n")

        cli_out = {
        }

        # validate_config(cli_out)
        formatted_json = json.dumps(cli_out, sort_keys=False, indent=2)

        click.echo("\nThis is your current settings file " +
                   click.style("config.json", bold=True) + ":\n")
        click.echo(click.style(formatted_json, fg="green", bold=True))

        confirm = input(
            "\nDoes this look good? (default 'y') [y/n]: ") or 'yes'
        if not to_bool(confirm):
            click.echo(
                "" + click.style("Please initialize skil CLI once again", fg="red", bold=True))
            return


def to_bool(string):
    if type(string) is bool:
        return string
    return True if string[0] in ["Y", "y"] else False


def handle():
    try:
        cli = CLI()
        sys.exit(cli.command_dispatcher())
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        click.echo(click.style("Error: ", fg='red', bold=True))
        traceback.print_exc()
        sys.exit()


def check_docker():
    devnull = open(os.devnull, 'w')
    try:
        subprocess.call(["docker", "--help"], stdout=devnull, stderr=devnull)
        click.echo(click.style(
            "Docker is running, starting installation.", fg="green", bold=True))
    except:
        click.echo(
            "" + click.style("Could not detect docker on your system. Make sure a docker deamon is running", fg="red", bold=True))
        raise Exception("Aborting installation, docker not found.")


if __name__ == '__main__':
    handle()
