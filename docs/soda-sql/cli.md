---
layout: default
title: Soda SQL CLI commands
description: Access a table of Soda SQL command-line interface commands. Use soda --help to review commands and options in your command-line interface.
sidebar: sql
parent: Soda SQL
redirect_from: /soda-sql/documentation/cli.html
---

# Soda SQL CLI commands


| Command               | Description |
| --------------------- | ----------- |
| `soda analyze` | Analyzes the contents of your data source and automatically prepares a scan YAML file for each dataset. Soda SQL puts the YAML files in the `/tables` directory inside the warehouse directory. |
| `soda create yourdatawarehouse` | Creates a new `warehouse.yml` file and prepares credentials in your `~/.soda/env_vars.yml`. Soda SQL does not overwrite or remove and existing environment variables, it only adds new.  |
| `soda ingest` | Ingests test result details from other tools, such as dbt. |
| `soda scan` | Uses the configurations in your scan YAML file to prepare, then run SQL queries against the data in your data source.  |

## List of commands

To see a list of Soda SQL command-line interface (CLI) commands, use the `soda` command.

Command:
```shell
$ soda
```

Output:
```shell
Usage: soda [OPTIONS] COMMAND [ARGS]...

  Soda CLI version 2.x.xxx

Options:
  --help  Show this message and exit.

Commands:
  analyze  Analyze tables and scaffold SCAN YAML
  create   Create a template warehouse.yml file
  ingest   Ingest test information from different tools
  scan     Compute metrics and run tests for a given table
```

## List of options

To see a list of configurable options for each command, use the command-line help.
```shell
$ soda create --help
$ soda analyze --help
$ ingest --help
$ soda scan --help
```

Refer to Run a Soda SQL scan for details and examples.


