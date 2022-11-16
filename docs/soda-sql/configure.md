
# Configure Soda SQL

After you [install Soda SQL](/docs/soda-sql/installation.md), you must create files and configure a few settings before you can run a scan.

## Overview of configuration 

1. Create a warehouse directory in which to store your warehouse YAML file and `/tables` directory.
2. Get Soda SQL to create a warehouse YAML file and an env_vars YAML file, then adjust the contents of each to input your data source connection details.
3. Get Soda SQL to discover all the datasets in your data source and create a scan YAML file for each dataset. The scan YAML files store the test criteria that Soda SQL uses to prepare SQL queries that scan your data source.
4. Adjust the contents of your new scan YAML files to add the tests you want to run on your data to check for quality.

Consider following the [Quick start tutorial](/docs/soda-sql-quick-start-soda-sql.md) that guides you through configuration and scanning.

## Configuration instructions

1. Use your command-line interface to create, then navigate to a new Soda SQL warehouse directory in your environment. The warehouse directory stores your warehouse YAML files and `/tables` directory. The example below creates a directory named `soda_warehouse_directory`.<br />

```shell
$ mkdir soda_warehouse_directory
$ cd soda_warehouse_directory
```
2. Use the data source-specific create command (see [list](#create-commands) below) to create and pre-populate two files that enable you to configure connection details for Soda SQL to access your data source:
* a `warehouse.yml` file which stores access details for your data source ([read more](/docs/soda-sql/warehouse.md))
* an `env_vars.yml` file which securely stores data source login credentials ([read more](/docs/soda-sql/warehouse.md))<br />

Use `soda create --help` for a list of all available data source types and options.
```shell
$ soda create warehousetype -d yourdbname -u dbusername -w soda_warehouse_directory 
```
3. Use a code editor to open the `warehouse.yml` file that Soda SQL created and put in your warehouse directory. Refer to [Datasource configuration](/docs/soda-sql/warehouse_types.md) to adjust the configuration details and authentication settings according to the type of data source you use, then save the file.
<br />
Example warehouse YAML
```yaml
name: soda_warehouse_directory
connection:
  type: postgres
  host: localhost
  username: env_var(POSTGRES_USERNAME)
  password: env_var(POSTGRES_PASSWORD)
  database: sodasql
  schema: public
```
4. Use a code editor to open the `env_vars.yml` that Soda SQL created and put in your local user home directory as a hidden file (`~/.soda/env_vars.yml`). Use the command `ls ~/.soda/env_vars.yml` to locate the file. Input your data source login credentials then save the file.
<br />
Example env_vars YAML
```yaml
soda_warehouse_directory:
  POSTGRES_USERNAME: someusername
  POSTGRES_PASSWORD: somepassword
```
5. In your command-line interface, use the `soda analyze` command to get Soda SQL to sift through the contents of your data source and automatically prepare a scan YAML file for each dataset. <br /><br />Soda SQL uses the name of the dataset to name each YAML file which it puts a new `/tables` directory in the warehouse directory. If you wish, you can set options to [include or exclude specific datasets](#add-analyze-options) during analysis.<br /> 
```shell
soda analyze
```
6. Use a code editor to open one of your new scan YAML files. Soda SQL pre-populated the YAML file with built-in metrics and tests that it deemed useful for the kind of data in the dataset. See [scan YAML](/docs/soda-sql/scan-yaml.md). <br /> Adjust the contents of the YAML file to define the tests that you want Soda SQL to conduct when it runs a scan on this dataset in your data source. Refer to [Metrics](/docs/soda-sql/sql_metrics.md) and [Tests](/docs/soda-sql/tests.md) for details. 
<br />
![configure yaml](/docs/assets/images/configure-yaml.png)

7. With your configuration complete, [run your first scan](/docs/soda-sql/scan.md).

#### Troubleshoot

**Problem:** When you run `soda analyze` you get an an authentication error. <br />
**Solution:** Check to see if you have another instance of Postgres already running on port 5432. If so, try stopping or uninstalling the Postgres instance, then run `soda analyze` again. 

## Create commands

Use `soda create --help` for a list of all available data source types and options.

|Warehouse type  | Command               |
|--------------- | --------------------- |
| Amazon Athena  | soda create athena    |
| Amazon Redshift| soda create redshift  |
| Apache Hive    | soda create hive      |
| Apache Spark   | soda create spark     |
| GCP Big Query  | soda create bigquery  |
| MS SQL Server  | soda create sqlserver |
| MySQL          | soda create mysql     |
| PostgreSQL     | soda create postgres  |
| Snowflake      | soda create snowflake |
| Trino          | soda create trino     |


## Add analyze options 

If you wish, you can define options for the `soda analyze` command that allow you exclude dataset(s) from the analysis or include specific dataset(s), or limit the number of datasets to anaylze. To do so, add one of the following options to the command.

| Option | Description and example
| --------- | ----------- | ------- |
| `-e TEXT` <br />or <br />`--exclude TEXT` | Replace `TEXT` with the case-insensitive name of the dataset(s) you wish to exclude from the analysis. Use a comma-separated list to include multiple datasets. Use `*` as a wild card. <br /> `soda analyze --exclude orders,customer` <br /> (If you need to exclude specific columns in a dataset during a Soda SQL scan, use the [`excluded_columns configuration key`](/docs/soda-sql/scan-yaml.md#scan-yaml-table-configuration-keys) in your scan YAML file.) |
| `-i TEXT` <br />or <br />`--include TEXT` | Replace `TEXT` with the case-insensitive name of the dataset(s) you wish to specifically analyze. Use a comma-separated list to include multiple datasets. Use `*` as a wild card. <br /> `soda analyze -i orders` |
| `-l INTEGER` <br />or <br />`--limit INTEGER` | Replace `INTEGER` with the number of datasets you want Soda SQL to analyze. <br /> `soda analyze --limit 10` |

