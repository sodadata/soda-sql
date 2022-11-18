# Define tests in Soda SQL

A **test** is a check that Soda SQL performs when it scans a dataset in your data source. Technically, it is a Python expression that, during a Soda SQL scan, checks metrics to see if they match the parameters you defined for a measurement. A single Soda SQL scan runs against a single dataset in your data source, but each scan can run multiple tests against multiple columns.

As a result of a [scan](/docs/soda-sql/scan.md), each test either passes or fails. When a test fails, it means that a property of the data in your dataset did not match the test parameters you defined. In other words, any test that returns `true` during a Soda SQL scan passes; any test that returns `false`, fails.

The **scan results** appear in your command-line interface (CLI). The results include an exit code which is an indicator of the test results: `0` means all tests passed; a non-zero value means one or more tests have failed.  See [Scan output in Soda SQL](/docs/soda-sql/scan.md#scan-output-in-soda-sql) for details.

**Soda Cloud** defines tests inside **monitors**. 

[Define tests using metrics](#define-tests-using-metrics)<br />
[Example tests using built-in metrics](#example-tests-using-built-in-metrics)<br />
[Example tests using custom metrics](#example-tests-using-custom-metrics)<br />
[Define names for tests](#define-names-for-tests)<br />
[Best practices for defining tests and running scans](#best-practices-for-defining-tests-and-running-scans)<br />
<br />

## Define tests using metrics

You define your tests in your [scan YAML file](/docs/soda-sql/scan-yaml.md) which is associated with a specific dataset in your data source. You can write tests using built-in [dataset metrics](/docs/soda-sql/sql_metrics.md#dataset-metrics) that Soda SQL applies to an entire dataset, or built-in [column metrics](/docs/soda-sql/sql_metrics.md#column-metrics) that Soda SQL applies to individual columns you identify. See [example tests](/docs/soda-sql/examples-by-metric.md) that use each built-in metric. 

You can also write tests using [custom metrics](/docs/soda-sql/sql_metrics.md#custom-metrics) (also known as SQL metrics) that you can apply to an entire dataset or to individual columns, or [historic metrics](/docs/soda-sql/metrics.md#historic-metrics) that access historic measurements in the Cloud Metric Store. 

Regardless of where it applies, each test is generally comprised of three parts:

- a metric (a property of the data in your data source)
- a comparison operator
- a value

For example:

```yaml
tests:
  - row_count > 0
```

At times, a test may only include one part, a metric, that simply returns a calculated value. For example, you may wish to write a test that simply returns the calculated sum of the values in a numeric column.

```yaml
columns:
  commission_paid:
    tests:
      - sum
```

However, where a test must determine whether or not data is valid, you must add a fourth element, a **column configuration key** to define what qualifies as valid. In the scan YAML file, you define a column configuration key before the test that will use the definition of "valid".

In the example below, the user defined the `valid_format` as `date_eu` or dd/mm/yyyy format. The metric `invalid_percentage` refers to the `valid_format` configuration key to determine if the data in the column is valid. Note that `valid_format` applies only to columns with data type TEXT. Refer to [Data types](/docs/soda-sql/supported-data-types.md) for details. 

To see a list of all available column configuration keys, see [Column configuration keys](/docs/soda-sql/sql_metrics.md#column-configuration-keys).

```yaml
columns:
    start_date:
        valid_format: date_eu
        tests:
            - invalid_percentage < 2.0
```

<br />

#### Example tests using built-in metrics

Reference the table below which corresponds to the following example scan YAML file. Both the `id` and `feepct` columns are of data type TEXT, enabling the user to define a `valid_format` for the contents of the columns. See [Valid format values](/docs/soda-sql/sql_metrics.md#valid-format-values) for details.

```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
tests:
  - row_count > 0
columns:
  id:
    valid_format: uuid
    tests:
      - invalid_percentage == 0
  feepct:
    valid_format: number_percentage
    tests:
      - invalid_percentage == 0
```

| Built-in metric | Comparison operator | Value | Applies to | Test |
| ------ | ------------------- | ----- | ---------- | ---- |
| `row_count` | `>` | `0` | whole dataset | Checks to see if the dataset has at least one row. If the test fails, it means the dataset has no rows, which means that the dataset is empty.|
| `invalid_percentage` | `==` | `0` | `id` column | Checks to see if all rows in the id column contain data in a valid format. If the test fails, it means that more than 0% of the rows contain invalid data, which is data that is in non-UUID format.|
| `invalid_percentage` | `==` | `0` | `feepct` column | Checks to see if all rows in the `feepct` column contain data in a valid format. If the test fails, it means that more than 0% of the rows contain invalid data, which is data that is not a numerical percentage.|

See [example tests](/docs/soda-sql/examples-by-metric.md) that use each built-in metric.

<br />



#### Example tests using custom metrics

If the built-in dataset and column metrics that Soda SQL offers do not quite give you the information you need from a scan, you can use **custom metrics** to customize your queries. Custom metrics essentially enable you to add SQL queries to your scan YAML file so that Soda SQL runs them during a scan. See [Custom metrics](/docs/soda-sql/sql_metrics.md#custom-metrics)

Reference the table below which corresponds to the following example scan YAML file.

```yaml
table_name: yourdataset
sql_metrics:
    - sql: |
          SELECT sum(volume) as total_volume_us
          FROM CUSTOMER_TRANSACTIONS
          WHERE country = 'US'
      tests:
          - total_volume_us > 5000
```

| Custom metric | Comparison operator | Value | Applies to | Test |
| ------------- | ------------------- | ----- | ---------- | ---- |
| `total_volume_us` | `>` | `5000`|  whole dataset | Checks to see if the sum of all customer transactions in the United States exceeds `5000`. If the test fails, it means that the total volume of transactions is less than `5000`.


## Define names for tests

Soda SQL can run both anonymous or named tests. If you intend to push Soda SQL scan results to your Soda Cloud account, a named tests appears in the Monitor Results table with the title you gave it; anonymous tests also appear, of course, but their name defaults to the test expression.

Example of an anonymous
```yaml
valid_format: number_percentage
tests:
    - invalid_percentage == 0
```

Examples of a named test
```yaml
valid_format: number_percentage
tests:
  - name: inval_percent
    expression: invalid_percentage == 0
    title: Invalid Percentage
```

## Best practices for defining tests and running scans

* Where you need to define tests that execute against <a href="https://www.guru99.com/fact-table-vs-dimension-table.html" target="_blank">facts and dimensions tables</a>, you can use [custom metrics](/docs/soda-sql/sql_metrics.md#custom-metrics) to join facts and dimensions using SQL statement to validate your business metrics. In general, write aggregation tests for facts tables and validity tests for data in dimensions tables.
* There is no limit to the number of tests that Soda SQL can run during a scan. 
* If you are using a [data orchestration tool](/docs/soda-sql/orchestrate_scans.md) to schedule regular Soda scans of your data, consider the frequency of change in your data streams, or how your data pipeline is scheduled. For example, if your data sources or streams provide new data in a batch once per day, schedule a Soda scan once per day after batch processing.
