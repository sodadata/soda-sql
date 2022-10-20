#!/usr/bin/env python
import sys
import pathlib
from setuptools import setup, find_namespace_packages

if sys.version_info < (3, 7):
    print("Error: Soda SQL requires at least Python 3.7")
    print("Error: Please upgrade your Python version to 3.7 or later")
    sys.exit(1)

package_name = "soda-sql-core"
# Managed by tbump - don't change manually
# And we can't have nice semver (<major>.<minor>.<patch>-<pre-release>-<build>)
# like "-alpha-1" as long as this is open >> https://github.com/pypa/setuptools/issues/2181
package_version = '2.2.2'
description = "Soda SQL Core"

long_description = (pathlib.Path(__file__).parent / "README.md").read_text()

requires = [

    "markupsafe==2.0.1",
    "Jinja2>=2.11.3, <4.0",
    "click>=8.0, <9.0",
    "pyyaml>=5.4.1",
    "requests>=2.23.0, <3.0",
    "Deprecated>=1.2.13, <1.3",
    "opentelemetry-api~=1.11.0",
    "opentelemetry-exporter-otlp-proto-http~=1.11.0",
    "protobuf~=3.19.0"
]
# TODO Fix the params
# TODO Add a warning that installing core doesn't give any warehouse functionality
setup(
    name=package_name,
    version=package_version,
    author="Tom Baeyens",
    author_email="tom@soda.io",
    description="Soda SQL library & CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(include=["sodasql*"]),
    install_requires=requires,
    entry_points={"console_scripts": ["soda=sodasql.__main__:main"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)
