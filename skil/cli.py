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
import click
from click.exceptions import ClickException
from dateutil import parser

from skil.experiments import Experiment
from skil.workspaces import WorkSpace
from skil.base import Skil
from skil.deployments import Deployment

from .config import DEFAULT_SKIL_CONFIG, save_skil_config

if sys.version_info[0] == 2:
    input = raw_input


def to_bool(string):
    if type(string) is bool:
        return string
    return True if string[0] in ["Y", "y"] else False


class CLI(object):

    def __init__(self):
        self.var_args = None
        self.command = None

        self.default_host = DEFAULT_SKIL_CONFIG['host']
        self.default_port = DEFAULT_SKIL_CONFIG['port']
        self.default_username = DEFAULT_SKIL_CONFIG['username']
        self.default_password = DEFAULT_SKIL_CONFIG['password']

    def command_dispatcher(self, args=None):
        desc = (
            'Pyskil - train, deploy and manage deep learning experiments with SKIL from Python.\n')
        parser = argparse.ArgumentParser(description=desc)
        parser.add_argument(
            '-v', '--version', action='version',
            version=pkg_resources.get_distribution("skil").version,
            help='Print pyskil version'
        )

        subparsers = parser.add_subparsers(title='subcommands', dest='command')
        subparsers.add_parser(
            'configure', help='Base configuration for pyskil. Run once')

        exp_parser = subparsers.add_parser(
            'init-experiment', help='Initialize a SKIL experiment from scratch.')
        exp_parser.add_argument(
            '-f', '--file', help='File to persist the experiment to.')

        dep_parser = subparsers.add_parser(
            'init-deployment', help='Initialize a SKIL deployment from scratch.')
        dep_parser.add_argument(
            '-f', '--file', help='File to persist the deployment to.')

        argcomplete.autocomplete(parser)
        args = parser.parse_args(args)
        self.var_args = vars(args)

        if not args.command:
            parser.print_help()
            return

        self.command = args.command

        if self.command == 'configure':
            self.configure()
            return

        if self.command == 'init-experiment':
            self.init_experiment(self.var_args['file'])
            return

        if self.command == 'init-deployment':
            self.init_deployment(self.var_args['file'])
            return

    def configure(self):

        click.echo(click.style(u"""\n██████╗ ██╗   ██╗███████╗██╗  ██╗██╗██╗     
██╔══██╗╚██╗ ██╔╝██╔════╝██║ ██╔╝██║██║     
██████╔╝ ╚████╔╝ ███████╗█████╔╝ ██║██║     
██╔═══╝   ╚██╔╝  ╚════██║██╔═██╗ ██║██║     
██║        ██║   ███████║██║  ██╗██║███████╗
╚═╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝ \n""", fg='blue', bold=True))

        click.echo(click.style("pyskil", bold=True) +
                   " train, deploy and manage deep learning experiments with SKIL from Python!\n")

        host = input("Specify your SKIL host address (default '%s'): " %
                     self.default_host) or self.default_host

        port = input("Specify your SKIL port (default '%s'): " %
                     self.default_port) or self.default_port

        username = input("Specify your SKIL user name (default '%s'): " %
                         self.default_username) or self.default_username

        password = input("Specify your SKIL password (default '%s'): " %
                         self.default_username) or self.default_username
        cli_out = {
            'host': host,
            'port': port,
            'username': username,
            'password': password
        }

        formatted_json = json.dumps(cli_out, sort_keys=False, indent=4)

        click.echo("\nThis is your current settings file " +
                   click.style(".skil", bold=True) + ":\n")
        click.echo(click.style(formatted_json, fg="green", bold=True))

        confirm = input(
            "\nDoes this look good? (default 'y') [y/n]: ") or 'yes'
        if not to_bool(confirm):
            click.echo(
                "" + click.style("Please initialize pyskil once again", fg="red", bold=True))
            return

        save_skil_config(cli_out)

    def init_experiment(self, file_name):
        if not file_name:
            file_name = 'experiment.json'
        path = os.path.join(os.getcwd(), file_name)
        if not os.path.isfile(path):
            experiment = Experiment()
            experiment.save(path)
        else:
            print('Warning: experiment file {} already exists'.format(file_name))

    def init_deployment(self, file_name):
        if not file_name:
            file_name = 'deployment.json'
        path = os.path.join(os.getcwd(), file_name)
        if not os.path.isfile(path):
            deployment = Deployment()
            deployment.save(path)
        else:
            print('Warning: deployment file {} already exists'.format(file_name))


def handle():
    try:
        cli = CLI()
        sys.exit(cli.command_dispatcher())
    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        click.echo(click.style("Error: ", fg='red', bold=True))
        traceback.print_exc(e)
        sys.exit()


if __name__ == '__main__':
    handle()
