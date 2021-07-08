"""
Copyright(c) 2021 Authors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files(the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
"""

import os
import logging

from awscli.customizations.commands import BasicCommand

from botocore.credentials import JSONFileCache

from .credentials import MFACredentialFetcher
from .credentials import MFACredentialPrinter


LOG = logging.getLogger(__name__)

CACHE_DIR = os.path.expanduser(os.path.join('~', '.aws', 'mfa', 'cache'))


class MFACrededntialProcessCommand(BasicCommand):
    NAME = 'cred-process'

    DESCRIPTION = 'describe the command'

    SYNOPSIS = ('aws mfa cred-process [--profile profile-name]')

    def _run_main(self, parsed_args, parsed_globals):
        raise NotImplementedError("to_cred_process not implemented yet")


class MFACredentialEnvCommand(BasicCommand):
    NAME = 'cred-env'

    DESCRIPTION = 'describe the command'

    SYNOPSIS = ('aws mfa cred-env [--profile profile-name]')

    def _run_main(self, parsed_args, parsed_globals):
        mfa_fetcher = MFACredentialFetcher(
            session=self._session,
            cache=JSONFileCache(CACHE_DIR)
        )

        cred = mfa_fetcher.fetch_credentials()
        printer = MFACredentialPrinter(cred)
        printer.to_cred_env()


class MFACommand(BasicCommand):
    NAME = 'mfa'

    DESCRIPTION = 'describe the command'

    SYNOPSIS = ('aws mfa <Command> [--profile profile-name]')

    SUBCOMMANDS = [
        {'name': 'cred-env', 'command_class': MFACredentialEnvCommand},
        {'name': 'cred-process', 'command_class': MFACrededntialProcessCommand},
    ]

    def _run_main(self, parsed_args, parsed_globals):
        self._raise_usage_error()
