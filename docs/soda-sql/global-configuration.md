# Soda SQL usage statistics

To understand how users are using Soda SQL, and to proactively capture bugs and performance issues, the Soda development team has added telemetry event tracking to Soda SQL. 

Soda tracks usage statistics using the Open Telemetry Framework. The data Soda tracks is completely anonymous, does not contain any personally identifiying information (PII) in any form, and is purely for internal use.

Soda SQL sends usage statistics whenever a user invokes it using any of its [commands](/docs/soda-sql/cli.md). Access [soda_telemetry.py](https://github.com/sodadata/soda-sql/blob/main/core/sodasql/telemetry/soda_telemetry.py) to see exactly how Soda collects usage statistics.

The table below lists the metrics and attributes that Soda currently tracks.

| Attribute or metric      | Derivation and notes                                                                                                      |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| `user_cookie_id`         | uuid generated once and stored in `~/.soda/config.yml`                                                                   |
| `command_name`           | Soda SQL command or API method name                                                                                       |
| `command_options`        | Soda SQL command or API method name                                                                                       |
| `version`                | version of soda-sql                                                                                                       |
| `datasource_type`        | name of the warehouse                                                                                                     |
| `datasource_id`          | hash of one of the following: <br />- host (Postgres, Redshift, Spark) <br />- account (Snowflake) <br />- project (BigQuery) <br />- and so on for other warehouse types |
| `sql_metrics_count`      | count of user-defined custom sql metrics                                                                                  |
| `historic_metrics_count` | count of user-defined historic metrics                                                                                  |
| `architecture`           | machine architecture                                                                                                      |
| `operating_system`       | operating system a user is using                                                                                          |
| `python_version`         | version of Python a user is using                                                                                         |
| `python_implementation`  | environment which provides support for executing Python programs                                                          |
| `invocation_start`       | span start from the Open Telemetry Framework                                                                              |
| `invocation_end`         | span end from Open Telemetry Framework                                                                                    |

## Opt out of usage statistics

Soda SQL collects usage statistics by default. You can opt-out from sending Soda SQL usage statistics at any time by adding the following to your `~/.soda/config.yml` file:
```
send_anonymous_usage_stats: false
```
