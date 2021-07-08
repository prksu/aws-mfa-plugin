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

import sys
import json
from hashlib import sha1

from botocore.credentials import CachedCredentialFetcher

from .exceptions import RequiredMFAConfigError


class MFACredentialPrinter(object):
    """ MFA temporary credential printer. """

    def __init__(self, credentials: dict):
        """
        :param credentials: credentials dictionary returned from MFACredentialFetcher.fetch_credentials().
        """
        self._credentials = credentials

    def to_cred_env(self):
        """ Print credential as environment variable.

        TODO: Detect shell 
        """
        print("export %s=%s;" % ("AWS_ACCESS_KEY_ID",
              self._credentials["access_key"]))
        print("export %s=%s;" % ("AWS_SECRET_ACCESS_KEY",
              self._credentials["secret_key"]))
        print("export %s=%s;" % ("AWS_SESSION_TOKEN",
              self._credentials["token"]))

    def to_cred_process(self):
        """ Print credential as aws credential_process format.

        UNIMPLEMENTED YET
        """
        raise NotImplementedError("to_cred_process not implemented yet")


class MFACredentialFetcher(CachedCredentialFetcher):
    """ MFA temporary credential fetcher. Subclass CachedCredentialFetcher """

    def __init__(self, session, cache=None, expiry_window_seconds=None):
        """
        :param session: The aws session.
        :param cache: An object that supports ``__getitem__``,
            ``__setitem__``, and ``__contains__``.  An example of this is
            the ``JSONFileCache`` class in aws-cli.
        """
        config = session.get_scoped_config()
        mfa_serial = config.get('mfa_serial')
        if mfa_serial is None:
            raise RequiredMFAConfigError(
                error_msg="missing mfa_serial in AWS_CONFIG file")
        self._mfa_serial = mfa_serial
        self._client_creator = session.create_client
        super(MFACredentialFetcher, self).__init__(
            cache, expiry_window_seconds
        )

    def _create_cache_key(self):
        """ Create a predictable cache key for the current configuration.

        The cache key is intended to be compatible with file names.
        """
        args = {
            'mfaSerial': self._mfa_serial,
        }

        args = json.dumps(args, sort_keys=True, separators=(',', ':'))
        argument_hash = sha1(args.encode('utf-8')).hexdigest()
        return self._make_file_safe(argument_hash)

    def _get_credentials(self):
        """ Get credentials by calling STS to get session token credentials. """

        """ NOTE: We use stderr for MFA Token input prompt 
        since we expected aws mfa (cred-env|cred-process) command
        has formatted output in stdout """
        prompt = "%s for (%s): " % ("MFA Token", self._mfa_serial)
        sys.stderr.write(prompt)
        sys.stderr.flush()
        mfa_token = input()
        client = self._client_creator('sts')
        response = client.get_session_token(
            SerialNumber=self._mfa_serial,
            TokenCode=mfa_token
        )

        return response
