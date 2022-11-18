# Scan YAML

A **scan** is a Soda SQL CLI command that uses SQL queries to extract information about data in a dataset.

Instead of laboriously accessing your data source and then manually defining SQL queries to analyze the data in datasets, you can use a much simpler Soda SQL scan. First, you configure scan metrics and tests in a **scan YAML** file, then Soda SQL uses the input from that file to prepare, then run SQL queries against your data.
<br />

[Create a scan YAML file](#create-a-scan-yaml-file)<br />
[Anatomy of the scan YAML file](#anatomy-of-the-scan-yaml-file)<br />
[Scan YAML table configuration keys](#scan-yaml-table-configuration-keys)<br />
[Add a dataset name for Soda Cloud](#add-a-dataset-name-for-soda-cloud)<br />

## Create a scan YAML file

You need to create a **scan YAML** file for every dataset in your data source that you want to scan. If you have 20 datasets in your data source, you need 20 YAML files, each corresponding to a single dataset.

You can create scan YAML files yourself, but the CLI command `soda analyze` sifts through the contents of your data source and automatically prepares a scan YAML file for each dataset. Soda SQL puts the YAML files in a `/tables` directory in your warehouse directory. (If you have not already created a warehouse YAML file, refer to the instructions in [Warehouse YAML](/docs/soda-sql/warehouse.md).)

In your command-line interface, navigate to the directory that contains your `warehouse.yml` file, then execute the following:

Command:

```shell
$ soda analyze
```

Output:

```shell
  | Analyzing warehouse.yml ...
  | Querying warehouse for tables
  | Creating tables directory tables
  | Executing SQL query:
SELECT table_name
FROM information_schema.tables
WHERE lower(table_schema)='public'
  | SQL took 0:00:00.008511
  | Executing SQL query:
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE lower(table_name) = 'demodata'
  AND table_catalog = 'sodasql'
  AND table_schema = 'public'
  | SQL took 0:00:00.013018
  | Executing SQL query:
  ...
    | SQL took 0:00:00.008593
  | Creating tables/demodata.yml ...
  | Next run 'soda scan warehouse.yml tables/demodata.yml' to calculate measurements and run tests
```
In the above example, Soda SQL created a scan YAML file named `demodata.yml` and put it in the `/tables` directory.

If you decide to create your own scan YAML files manually, best practice dictates that you name the YAML file using the same name as the dataset in your warehouse.

#### Tip!
Use the `soda analyze --help` command to review options you can include to customize the analysis. For example, use `soda analyze --include customer` to analyze only the dataset named `customer` in your data source. 

## Anatomy of the scan YAML file

When it creates your scan YAML file, Soda SQL pre-populates it with the `test` and `metric` configurations it deems useful based on the data in the dataset it analyzed. You can keep those configurations intact and use them to run your scans, or you can adjust or add to them to fine-tune the tests Soda SQL runs on your data.

The following describes the contents of a scan YAML file that Soda SQL created and pre-populated.

![scan-anatomy](/docs/assets/images/scan-anatomy.png)


**1** - The value of **table_name** identifies a dataset in your data source. If you were writing a SQL query, it would be the value you would supply for your `FROM` statement.

**2** - A **metric** is a property of the data in your data source.  A **measurement** is the value for a metric that Soda SQL checks against during a scan. For example, in the test `row_count = 5`, `row_count` is the metric and `5` is the measurement.

**3** - A **test** is a Python expression that, during a scan, checks metrics to see if they match the parameters defined for a measurement. As a result of a scan, a test either passes or fails.

For example, the test `row_count > 0` checks to see if the dataset has at least one row. If the test passes, it means the dataset has at least one row; if the test fails, it means the dataset has no rows, which means that it is empty. Tests in this part of the YAML file apply to all columns in the dataset. A single Soda SQL scan can run many tests on the contents of the whole dataset.

**4** - A **column** identifies a specific column in your dataset. Use column names to configure tests against individual columns in the dataset. A single Soda SQL scan can run many tests in many columns.

**5** - **`id`** and **`feepct`** are column names that identify specific columns in the dataset this scan YAML file scans.

**6** - The value of the **column configuration key** `valid_format` identifies the only form of data in the column that Soda SQL recognizes as valid during a scan. In this case, any row in the `id` column that contains data that is in UUID format (universally unique identifier) is valid; anything else is invalid. Refer to [Column configuration keys](/docs/soda-sql/sql_metrics.md#column-configuration-keys) for more detail.

**7** - Same as above, except the tests in the `column` section of the YAML file run only against the contents of the single, identified column. In this case, the test `invalid_percentage == 0` checks to see if all rows in the `id` column contain data in a valid format. If the test passes, it means that 0% of the rows contain data that is invalid; if the test fails, it means that more than 0% of the rows contain invalid data, which is data that is in non-UUID format.

## Scan YAML table configuration keys

The table below describes all of the table-level **configuration keys** you can use to customize your scan.

| Key         | Description | Required |
| ----------- | ----------- | -------- |
| `columns` | The section of the scan YAML file in which you define tests and metrics that apply to individual columns. See [Column metrics](/docs/soda-sql/sql_metrics.md#column-metrics) for configuration details.| optional |
| `excluded_columns` | Identifies the columns against which Soda SQL does NOT execute tests during a scan. Identifies columns by name. Use `excluded_columns` to avoid scanning columns that contain sensitive or personally identifiable information (PII). Specify columns that Soda SQL should *not* scan and send to Soda Cloud as [samples of rows](/docs/soda-sql/samples.md) or [failed rows](/docs/soda-sql/send-failed-rows.md). See [Excluded columns example](#excluded-columns-example) below. <br /> On a related note, you can specify datasets to [exclude or include](/docs/soda-sql/configure.md#add-analyze-options) during `soda analyze`.| optional |
| `filter` | A SQL expression that Soda SQL adds to the `WHERE` clause in the query. Use `filter` to pass variables, such as date, into a scan. Uses [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) as the templating language. See [Apply filters](/docs/soda-sql/filtering.md) for configuration details.| optional |
| `frequent_values_limit` | Defines the maximum number of elements for the `maxs` metric. Default value is `5`.| optional |
| `metrics` |  A list of all the built-in metrics that you can use to configure a scan. This list includes both dataset and column metrics. See [Configure metrics in Soda SQL](/docs/soda-sql/sql_metrics.md) for configuration details.| optional |
| `mins_maxs_limit` | Defines the maximum number of elements for the `mins` metric. Default value is `5`.| optional |
| `samples` | Defines a threshold on the number of sample rows that Soda SQL sends to Soda Cloud. See [Send sample data to Soda Cloud](/docs/soda-sql/samples.md) and [Send failed rows to Soda Cloud](/docs/soda-sql/send-failed-rows.md). | optional |
| `sql_metrics` | The section of the scan YAML file in which you define custom sql queries to run during a scan. You can apply `sql_metrics` to all data in the dataset, or data in individual columns. See [Custom metrics](/docs/soda-sql/sql_metrics.md#custom-metrics) for configuration details.| optional |
| `table_name` | Identifies a dataset in your data source. | required |

#### Excluded columns example

```yaml
table_name: orders
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - ...
excluded_columns:
  - discount
  - productid
tests:
  - row_count > 0
columns:
  orderid:
    valid_format: uuid
    tests:
      - invalid_percentage <= 3
```

## Add a dataset name for Soda Cloud

If you have [connected Soda SQL to your Soda Cloud account](/docs/soda-sql/connect_to_cloud.md), you have the option of adding a `dataset_name` identifier to your scan YAML file. Soda SQL sends the value of this identifier to Soda Cloud along with any test results so that viewers in Soda Cloud can more precisely identify to which dataset the results pertain.

Scan YAML:
```yaml
table_name: orders
dataset_name: Orders in EMEA
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - ...
tests:
  - row_count > 0
```

Soda Cloud Datasets dashboard:

![named-dataset2](/docs/assets/images/named-dataset2.png)


Soda Cloud Monitor info:

![named-dataset1](/docs/assets/images/named-dataset1.png)

<br />

Further, you can use a variable in the `dataset_name` identifier so that Soda SQL dynamically retrieves information from the `soda scan` command and uses it in the identifier. Include a variable in the `dataset_name` as in the example that follows, then use the `-v` option to provide a value for the variable at scan time. 

Scan YAML:
```yaml
table_name: orders
dataset_name: Orders in {% raw{{ region }}{% endraw
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - ...
tests:
  - row_count > 0
```
Scan command:
```shell
soda scan warehouse.yml tables/orders.yml -v region=APAC
```

Soda Cloud Datasets dashboard:

![named-dataset3](/docs/assets/images/named-dataset3.png) 
