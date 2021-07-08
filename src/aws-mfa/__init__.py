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


from botocore.session import Session

from .command import MFACommand


def awscli_initialize(cli):
    """ Entry point called by awscli """
    cli.register('building-command-table.main', register_mfa_command)


def register_mfa_command(command_table, session: Session, **kwargs):
    """ Register mfa command """
    command_table['mfa'] = MFACommand(session)
