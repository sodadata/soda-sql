# Install Soda SQL

Soda SQL is a command-line interface (CLI) tool that enables you to scan the data in your data source to surface invalid, missing, or unexpected data.

[Compatibility](#compatibility)<br />
[Requirements](#requirements)<br />
[Install](#install)<br />
[Upgrade](#upgrade)<br />
[Troubleshoot](#troubleshoot)<br />


## Compatibility

Use Soda SQL to scan a variety of data sources:<br />

<table>
  <tr>
    <td>Amazon Athena<br /> Amazon Redshift<br /> Apache Hive (experimental)<br /> Apache Spark<br/> GCP Big Query<br /></td>
    <td> MySQL (experimental) <br />Microsoft SQL Server (experimental) <br /> PostgreSQL<br /> Snowflake<br /> Trino (Experimental)<br /></td>
  </tr>
</table>


## Requirements

To use Soda SQL, you must have installed the following on your system.

* **Python 3.7** or greater. To check your existing version, use the CLI command: `python --version`
* **Pip 21.0** or greater. To check your existing version, use the CLI command: `pip --version`

For Linux users only, install the following:
* On Debian Buster: `apt-get install g++ unixodbc-dev python3-dev libssl-dev libffi-dev`
* On CentOS 8: `yum install gcc-c++ unixODBC-devel python38-devel libffi-devel openssl-devel`

For MSSQL Server users only, install the following:
* [SQLServer Driver](https://docs.microsoft.com/en-us/sql/connect/odbc/microsoft-odbc-driver-for-sql-server?view=sql-server-ver15)



## Install

From your command-line interface tool, execute the following command, replacing `soda-sql-athena` with the install package that matches the type of data source you use to store data.

```
$ pip install soda-sql-athena
```

| Data source                  | Install package    |
| ---------------------------- | ------------------ |
| Amazon Athena                | soda-sql-athena    |
| Amazon Redshift              | soda-sql-redshift  |
| Apache Hive (Experimental)   | soda-sql-hive      |
| Apache Spark                 | soda-sql-spark     |
| GCP Big Query                | soda-sql-bigquery  |
| MS SQL Server (Experimental) | soda-sql-sqlserver |
| MySQL (Experimental)         | soda-sql-mysql     |
| PostgreSQL                   | soda-sql-postgresql|
| Snowflake                    | soda-sql-snowflake |
| Trino (Experimental)         | soda-sql-trino     |


Optionally, you can install Soda SQL in a virtual environment. Execute the following commands one by one:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install soda-sql-yourdatasource
```

To deactivate the virtual environment, use the command: `deactivate`.

## Upgrade

To upgrade your existing Soda SQL tool to the latest version, use the following command replacing `soda-sql-athena` with the install package that matches the type of data source you are using.
```shell
pip install soda-sql-athena -U
```

## Troubleshoot

**Problem:** There are known issues on Soda SQL when using pip version 19. <br />
**Solution:** Upgrade `pip` to version 20 or greater using the following command:
```shell
$ pip install --upgrade pip
```
<br />

**Problem:** Upgrading Soda SQL does not seem to work. <br />
**Solution:** Run the following command to skip your local cache when upgrading your Soda SQL version:
```shell
$ pip install --upgrade --no-cache-dir soda-sql-yourdatasource
```
<br />

**Problem:** I can't run the `soda` command in my CLI. It returns `command not found: soda`. <br />
**Solution:** If you followed the instructions to [install Soda SQL](/docs/soda-sql/installation.md) and still received the error, you may need to adjust your `$PATH` variable. 
1. Run the following command to find the path to your installation of Python, replacing `soda-sql-postgresql` with the install package that matches the type of warehouse you use if not PostgreSQL:<br />
`pip show soda-sql-postgresql`
<br /> <br /> The output indicates the Location that looks something like this example:
```shell
...
Location: /Users/yourname/Library/Python/3.8/lib/python/site-packages
...
```
2. Add the location to your `$PATH` variable using the `export PATH` command as follows:<br />
`'export PATH=$PATH:/Users/yourname/Library/Python/3.8/bin soda'`
3. Run the `soda` command again to receive the following output:<br />
```shell
Usage: soda [OPTIONS] COMMAND [ARGS]...
  Soda CLI version 2.1.xxx
Options:
  --help  Show this message and exit.
Commands:
  analyze  Analyze tables and scaffold SCAN YAML
  create   Create a template warehouse.yml file
  ingest   Ingest test information from different tools
  scan     Compute metrics and run tests for a given table
```