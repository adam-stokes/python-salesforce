"""Placeholder for scripts to inherit cli interface
"""

import argparse
import sys
import logging
import json
from sforce.client import sf_session
from sforce.models import Account, Case

class CMD(object):
    def __init__(self, commons):
        self.commons = commons
        self.args = self.parse_options(sys.argv)
        self.session = sf_session(self.commons)
        if self.args.debug:
            logging.getLogger().setLevel(logging.DEBUG)

    def cmd_account(self, options):
        """ parses account cli
        """
        logging.debug("Running Account Queries")
        acct = Account(self.commons)
        if options.id:
            print(json.dumps(acct.by_id(options.id)))
        if options.name:
            print(json.dumps(acct.by_name(options.name)))

    def cmd_case(self, options):
        """ parses case cli
        """
        case = Case(self.commons)
        if options.number:
            print(json.dumps(case.by_id(options.number, True)))
            

    def parse_options(self, *args, **kwds):
        parser = argparse.ArgumentParser(description='Salesforce CLI',
                                         prog='sf-cli')
        subparsers = parser.add_subparsers(title='subcommands',
                                           description='valid subcommends',
                                           help='additional help')
        # Account

        parser_a = subparsers.add_parser('account', help='Query Account help')
        parser_a.add_argument('--id', dest='id', help='Account ID')
        parser_a.add_argument('--name', dest='name', help='Account Name')
        parser_a.set_defaults(func=self.cmd_account)

        # Case
        parser_b = subparsers.add_parser('case', help='Query Case help')
        parser_b.add_argument('--number', dest='number', help='Case number to lookup')
        parser_b.set_defaults(func=self.cmd_case)

        # Debug
        parser.add_argument('-d', '--debug', action='store_true',
                            dest='debug', default=False, help='Run in debug mode')

        return parser.parse_args()

    def run(self):
        self.args.func(self.args)
