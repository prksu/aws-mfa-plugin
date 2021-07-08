"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name="aws-mfa-plugin",
    version="0.0.3",
    description="An awscli plugin to authenticate and retrive AWS temporary credentials using a MFA device",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/prksu/aws-mfa-plugin",
    author="Ahmad Nurus S.",
    author_email="ahmadnurus.sh@gmail.com",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='aws, aws-mfa, aws-cli, aws-cli-plugins, aws-mfa-plugin',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=[],
    project_urls={
        'Bug Reports': 'https://github.com/prksu/aws-mfa-plugin/issues',
        'Source': 'https://github.com/prksu/aws-mfa-plugin/',
    },
)
