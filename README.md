# AWS MFA Plugin

An awscli plugin to authenticate and retrive AWS temporary credentials using a MFA device.

## Installation

This plugin was published in [pypi.org](https://pypi.org/project/aws-mfa-plugin/). So the installation can be done using pip.

```shell
$ pip3 install --user aws-mfa-plugin
```

> *NOTE: We recommend installing inside user-site*


### Configure the plugin

If you are using awscli v1 configuring plugin is pretty simple.

```shell
$ aws configure set plugins.mfa aws-mfa
```

Otherwise, If you are using awscli v2, there is a need for additional config. [see](https://docs.aws.amazon.com/cli/latest/userguide/cliv2-migration.html#cliv2-migration-profile-plugins) for more details.

```shell
$ aws configure set plugins.cli_legacy_plugin_path $(python3 -m site --user-site)
```

> *Assumed the plugin installed inside user-site* 

### Verify plugin installation

If you configure correctly the plugin will become a subcommand of `aws` command.

```shell
$ aws mfa
```

## Getting Started

Before using this plugin to retrieve temporary credentials you need to configure mfa_serial device.

```shell
$ aws configure set mfa_serial <your-mfa-serial-device>
```

To retrive temporary credentials

```shell
$ aws mfa cred-env
MFA Token for (arn:aws:iam::1234567890:mfa/username): 123456
export AWS_ACCESS_KEY_ID=<access-key-id>
export AWS_SECRET_ACCESS_KEY=<access-secret-key>
export AWS_SESSION_TOKEN=<token>
```

Or you can directly set these temporary credentials as environment variable by using `eval` command

```shell
$ eval $(aws mfa cred-env)
MFA Token for (arn:aws:iam::1234567890:mfa/username): 123456
```

## License

This project licensed under MIT LICENSE, see [LICENSE](https://github.com/prksu/aws-mfa-plugin/blob/main/LICENSE).
