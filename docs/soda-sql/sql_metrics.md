# Configure metrics in Soda SQL

A **metric** is a property of the data in your database. A **measurement** is the value for a metric that Soda SQL checks against during a scan. The following sections detail the configuration for metrics you can customize in your [scan YAML file](/docs/soda-sql/scan-yaml.md).

Read more about [Metrics](/docs/soda-sql/metrics.md) in general as they apply to both Soda SQL and Soda Cloud. 

[Dataset metrics](#dataset-metrics)
[Column metrics](#column-metrics)
[Using regex with column metrics](#using-regex-with-column-metrics)
[Column configuration keys](#column-configuration-keys) 
[Valid format values](#valid-format-values) 
[Historic metrics](#historic-metrics)
[Metric groups and dependencies](#metric-groups-and-dependencies)
[Custom metrics](#custom-metrics)
[Custom metric names](#custom-metric-names)
[GROUP BY queries in custom metrics](#group-by-queries-in-custom-metrics)
[Variables in custom metrics](#variables-in-custom-metrics)
[Custom metrics using file reference](#custom-metrics-using-file-reference)
<br />

## Dataset metrics

Use **dataset metrics** to define tests in your scan YAML file that execute against all data in the dataset during a scan.

![table-metrics](/docs/assets/images/table-metrics.png)

| Dataset metric <br />in Soda SQL | Description      |
| ---------- | ---------------- | -------------|
| `row_count` | The number of rows in a dataset. |
| `schema` | A list of column names in a dataset, and their data types. |


#### Example tests using a dataset metric

```yaml
tests:
  - row_count > 0
```
Checks to see if the dataset has more than one row. The test passes if the dataset contains rows.

<br />

```yaml
tests:
  - row_count =5
```
Checks to see if the dataset has exactly five rows. The test fails if the dataset contains more or fewer than five rows.


## Column metrics

Use **column metrics** to define tests in your scan YAML file that execute against specific columns in a dataset during a scan. 

Where a column metric references a valid or invalid value, or a limit, use the metric in conjunction with a **column configuration key**. A Soda SQL scan uses the value of a column configuration key to determine if it should pass or fail a test. See [example](#example-tests-using-a-column-metric) below.

![column-metrics](/docs/assets/images/column-metrics.png)


See [Metrics examples](/docs/soda-sql/examples-by-metric.md).

| Column metric<br /> in Soda SQL | Column metric<br /> in Soda Cloud |Description |  Applies to [data type](/docs/soda-sql/supported-data-types.md) | Column config key(s) / Validity Rule(s) | 
| ----------------------- | ----------- | --------------------- | ----------------------------- | ----------------------------- |
| `avg`| Average | The calculated average of the values in a numeric column. | number |  - | 
| `avg_length` | Average Length | The average length of string values in a column.  | text  |  -  |
| `distinct`<sup>1</sup> | Distinct Values | The number of rows that contain distinct values, relative to the column. | number | - | 
| `duplicate_count`<sup>1</sup>| Duplicate Values | The number of rows that contain duplicate values, relative to the column. | text, number, time  | - |
| `frequent_values`<sup>1</sup> | Top Values | A list of values in the column and the frequency with which they occur. | text, number, time  | - |
| `histogram`<sup>1</sup> | Histogram | A list of values to use to create a histogram that represents the contents of the column. | number | - |
| `invalid_count` | Invalid Values | The number of rows that contain invalid values. | text, number, time  | `valid_format` <br /> `valid_regex`<sup>2</sup> <br /> `valid_values` <br /> `valid_min_length` <br /> `valid_max_length`|
| `invalid_percentage` | Invalid Values (%) |The percentage of rows that contain invalid values.  | text, number, time  |  `valid_format` <br /> `valid_regex`<sup>2</sup> <br />`valid_values`<br /> `valid_min_length` <br /> `valid_max_length` |
| `max` | Maximum Value | The greatest value in a numeric column. |  number, time  |  -  |
| `max_length` | Maximum Length | The maximum length of string values in a column. |  text  |  -  |
| `maxs`<sup>1</sup> | Maxs | A list of values that qualify as maximum relative to other values in the column. | text, number, time | - |
| `min` | Minimum Value | The smallest value in a numeric column.  | number, time |  -  |
| `min_length` | Minimum Length | The minimum length of string values in a column.  | text  |  -  |
| `mins`<sup>1</sup> | Mins | A list of values that qualify as minimum relative to other values in the column. | text, number, time | - |
| `missing_count` | Missing Values | The number of rows in a column that do not contain specific content. | text, number, time  | `missing_format` <br /> `missing_regex`<sup>2</sup>  <br /> `missing_values`  |
| `missing_percentage` | Missing Values (%) | The percentage of rows in a column that do not contain specific content. | text, number, time  | `missing_format` <br /> `missing_regex`<sup>2</sup>  <br /> `missing_values`|
| `row_count` | n/a | The number of rows in a column. |  text, number, time | - |
| `stddev` | Standard Deviation | The calculated standard deviation of values in a numeric column. | number | - |
| `sum` | Sum | The calculated sum of the values in a numeric column.   | number | -  |
| `unique_count`<sup>1</sup> | Unique Values | The number of rows in which a value appears exactly only once in the column. | text, number, time | - |
| `uniqueness`<sup>1</sup> | Uniqueness (%) | A ratio that produces a number between 0 and 100 that indicates how unique the data in a column is. 0 indicates that all the values are the same; 100 indicates that all the values in the column are unique. | text, number, time | - |
| `valid_count` |  Valid Values | The number of rows that contain valid content.  | text, number, time  | `valid_format` <br /> `valid_regex`<sup>2</sup>  <br /> `valid_values` <br /> `valid_min_length` <br /> `valid_max_length` |
| `valid_percentage` | n/a | The percentage of rows that contain valid content.  |  text, number, time |  `valid_format` <br /> `valid_regex`<sup>2</sup>  <br /> `valid_values` <br /> `valid_min_length` <br /> `valid_max_length` |
| `values_count` | Values | The number of rows that contain content included in a list of valid values. |  text, number, time | `valid_values` <br /> `valid_regex`<sup>2</sup>  |
| `values_percentage` | Values (%) | The percentage of rows that contain content identified by valid values. | text, number, time | `valid_values` <br /> `valid_regex`<sup>2</sup>  |
| `variance` | Variance | The calculated variance of the values in a numeric column.  | number, time  | - |

<sup>1</sup> When configuring these metrics in Soda SQL, you must also define a [metric group](/docs/soda-sql/sql_metrics.md#metric-groups-and-dependencies) in the scan YAML file. <br />
<sup>2</sup> Learn more about [using regex with column metrics](#using-regex-with-column-metrics).

### Using regex with column metrics

* You can only use regex to define valid or missing values in columns that contain strings.
* When using regex to define valid or missing values, be sure to put the regex inside single quotes, as per the following example. You must single quotes because, as per YAML convention, chars like `[` and `]` have specific meaning in YAML if they are the first char of a value. If the first char is a normal text char then the YAML parser reads the rest of the value as a string.
```yaml
firstname:
    valid_regex: '[A-Z].'
    tests:
      - invalid_count == 0
```

### Column configuration keys

The column configuration key:value pair defines what Soda SQL ought to consider as "valid" or "missing".  Refer to [Using regex with column metrics](#using-regex-with-column-metrics) for important details on how to define the regex in a YAML file.

| Column config key(s) / Validity Rule(s)  | Description  | Values |
| ------------------------- | ------------ | ------ |
| `metric_groups` | Only available in Soda SQL. <br />Specifies pre-defined groups of metrics that Soda computes for this column. See [Metric groups and dependencies](/docs/soda-sql/sql_metrics.md#metric-groups-and-dependencies) for details.| `duplicates` <br /> `length` <br /> `missing`  <br /> `profiling` <br /> `statistics` <br /> `validity` |
| `missing_format` | Defines what qualifies as a value that ought to register as missing, such as whitespace or empty strings. For example, three spaces in row is recognizable as an entry, but from a business perspective, it ought to be recognized as empty. |   |
| `missing_regex` | Use regex expressions to specify your own custom missing values.| regex, no forward slash delimiters, string only |
| `missing_values` | Specifies the values that Soda is to consider missing in list format.| values in a list |
| `valid_format` | Specifies a named valid text format. Can apply only to columns using data type TEXT. See [Data types](/docs/soda-sql/supported-data-types.md). | See [Valid format values](#valid-format-values) table.  |
| `valid_max` | Specifies a maximum value for valid values. | integer or float|
| `valid_max_length` | Specifies a maximum string length for valid values. | string |
| `valid_min` | Specifies a minimum value for valid values. | integer or float |
| `valid_min_length` | Specifies a minimum string length for valid values. | string |
| `valid_regex` | Use regex expressions to specify your own custom valid values. | regex, no forward slash delimiters, string only |
| `valid_values` | Specifies several valid values in list format. | values in a list |


### Valid format values

Valid formats are experimental and subject to change.<br />
**Valid formats apply *only* to columns using data type TEXT.** See [Data types](/docs/soda-sql/supported-data-types.md).

| Valid format value <br />  | Format |
| ----- | ------ |
| `credit_card_number` | Four four-digit numbers separated by spaces.<br /> Four four-digit numbers separated by dashes.<br /> Sixteen-digit number.<br /> Four five-digit numbers separated by spaces.<br />|
| `date_eu` | Validates date only, not time. <br />dd/mm/yyyy |
| `date_inverse` | Validates date only, not time. <br />yyyy/mm/dd |
| `date_iso_8601` | Validates date and/or time according to <a href="https://www.w3.org/TR/NOTE-datetime" target="_blank">ISO 8601 format </a>. <br /> 2021-04-28T09:00:00+02:00 |
| `date_us` | Validates date only, not time. <br />mm/dd/yyyy |
| `email` | name@domain.extension |
| `ip address` | Four whole numbers separated by `.` |
| `ipv4 address` | Four whole numbers separated by `.` |
| `ipv6 address` | Eight values separated by `:` |
| `number_decimal_comma` | Number uses `,` as decimal indicator.|
| `number_decimal_point` | Number uses `.` as decimal indicator.|
| `number_money` | Format matches any of the `number_money_` patterns listed below.|
| `number_money_chf` | Number matches Swiss franc currency pattern. |
| `number_money_eur` | Number matches Euro currency pattern. |
| `number_money_gbp` | Number matches British pound currency pattern. |
| `number_money_rmb` | Number matches Renminbi yuan currency pattern. |
| `number_money_usd` | Number matches US dollar currency pattern. |
| `number_percentage` | Number is a percentage. |
| `number_percentage_comma` | Number is a percentage with a `,` decimal indicator. |
| `number_percentage_point` | Number is a percentage with a `.` decimal indicator. |
| `number_whole` | Number is whole. |
| `phone_number` | +12 123 123 1234<br /> 123 123 1234<br /> +1 123-123-1234<br /> +12 123-123-1234<br /> +12 123 123-1234<br /> 555-2368<br /> 555-ABCD |
| `time` | 11:59:00,000<br /> 11:59:00<br /> 11:59<br /> 11-59-00,000<br /> 23:59:00,000<br /> Noon<br /> 1,159 |
| `time_12h` | Validates against the 12-hour clock. <br /> 11:00 |
| `time_24h` | Validates against the 24-hour clock. <br /> 23:00 |
| `uuid` | Universally unique identifier. |




#### Example tests using a column metric

```yaml
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
`invalid_percentage == 0` in column `id` with column configuration `valid_format: uuid` checks the rows in the column named `id` for values that match a uuid (universally unique identifier) format. If the test passes, it means that 0% of the rows contain data that is invalid; if the test fails, it means that more than 0% of the rows contain invalid data, which is data that is in non-UUID format.

`invalid_percentage == 0` in column `feepct` with column configuration `valid_format: number_percentage` checks the rows in the column named `feepct` for values that match a percentage format. If the test passes, it means that 0% of the rows contain data that is invalid; if the test fails, it means that more than 0% of the rows contain invalid data, which is data that is in non-percentage format.

See more examples of how to use *all* column metrics in [Examples by metric](/docs/soda-sql/examples-by-metric.md).


## Historic metrics

When you run a scan using Soda SQL, it displays the scan results in the command-line where you can review the results of tests that passed or failed. These results are ephemeral; Soda SQL does not store them. 

If your Soda SQL instance is [connected to a Soda Cloud account](/docs/soda-sql/connect_to_cloud.md), Soda SQL also pushes the scan results to Soda Cloud where they appear in a table of **Monitor Results**. Soda Cloud stores the measurements resulting from each test Soda SQL executes against the data in the Cloud Metric Store. It uses these stored measurements to display the metric's history in a graph that shows you changes over time.

In Soda SQL, you can define **historic metrics** so that you can write tests in scan YAML files that test data relative to the historic measurements contained in the Cloud Metric Store. Essentially, this type of metric allows you to use Soda SQL to access the historic measurements in the Cloud Metric Store and write tests that use those historic measurements. 

To use `historic_metrics`, refer to the following example scan YAML file and the table below.

```yaml
table_name: orders.yml
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - ...
columns:
  ID:
    metrics:
      - distinct
      - duplicate_count
      - valid_count
      - avg
    historic_metrics:
      #avg of last 7 measurements
      - name: avg_dup_7
        type: avg
        metric: duplicate_count
        count: 7
      # min of last 30 measurements
      - name: distinct_min_30
        type: min
        metric: distinct
        count: 30
      # single previous measurement
      - name: prev_valid_count
        type: prev
        metric: valid_count
        count: 1
      # 7 measurements ago
      - name: prev_valid_count_7
        type: prev
        metric: valid_count
        count: 7
    tests:
      - duplicate_count < avg_dup_7
      - distinct < distinct_min_30
      - valid_count > prev_valid_count_7
      - valid_count > prev_valid_count
```

| Historic metric property | Required? | Use                                                 | Accepted input |
| ------------------------ | --------- |---------------------------------------------------- | ----------------|
| `name`                   | required  | Provide a name for your metric. | string        | 
| `type`                   | required  | Identify the aggregation type.                      | `avg` <br /> `max` <br /> `min` <br /> `prev` |
| `metric`                 | required  | Identify the metric from which to aggregate measurements. | `avg` <br /> `distinct` <br /> `duplicate_value` <br /> `valid_count` |
| `count`                  | required  | Use with `avg`, `max`, or `min` to define the number of measurements to aggregate. <br /> <br /> Use with `prev` to define the number of previous measurements to count back to. For example, if the value is `7`, Soda Cloud counts back to the measurement that appeared as the result seven scans ago and uses that value as the historic measurement in the current test.| integer |

#### Troubleshoot

**Problem:** When using an historic metric, you get an scan error message that advises you that there are insufficient measurements to complete the scan.

**Solution:** The Cloud Metric Store does not contain enough historic measurements to execute the test you have defined. For example, if you defined a test to count back to the seventh historic measurement but your Cloud Metric Store only contains three historic measurements, Soda SQL cannot complete the scan. Consider lowering the count-back number in your test, then run the scan again.


## Metric groups and dependencies

Out of the box, Soda SQL includes a **metric groups** configuration key. Define this configuration key in your scan YAML file in the dataset level or column level so that when you use one of the group's metrics in a test, Soda SQL automatically runs the test against all the metrics in its group.

| `metric_groups` value | Metrics the scan includes |
| ------------------- | ----------------------- |
| `all` | all column metrics groups |
| `missing` | `missing_count`, `missing_percentage`, `values_count`, `values_percentage`. |
| `validity` |  `valid_count`, `valid_percentage`, `invalid_count`, `invalide_percentage` |
| `duplicates` | `distinct`, `unique_count`, `duplicate_count`, `uniqueness` |
| `length` | `min_length`, `max_length`, `avg_length` |
| `profiling` |  `maxs`, `mins`, `frequent_values`, `histogram` |
| `statistics` | `min`, `max`, `avg`, `sum`, `variance`, `stddev` |


To use these metrics, be sure to define the `metric_groups` in your scan YAML file at the dataset level if the test is to apply to all columns in a dataset, or at the column level if the test is to apply only to a single column. An example follows, below.

| Column metric  |  Description |  Use with `metric_groups` |
| -------------- | ------------ | ------------------------- |
| `distinct` |  The number of rows that contain distinct values, relative to the column. For example, where a column has values: `aaa`, `aaa`, `bbb`, `ccc`, it has three distinct values. | duplicates |
| `duplicate_count` | The number of rows that contain duplicate values, relative to the column. | duplicates |
| `frequent_values` |  A list of values in the column and the frequency with which they occur.  |  profiling |
| `histogram` |  A list of values to use to create a histogram that represents the contents of the column.  |  profiling  |
| `maxs` |  A list of values that qualify as maximum relative to other values in the column.  |  profiling |
| `mins` |  A list of values that qualify as minimum relative to other values in the column.  |  profiling |
| `unique_count` | The number of rows in which a value appears exactly only once in the column. For example, where a column has values: `aaa`, `aaa`, `bbb`, `ccc`, it has two unique values.  | duplicates |
| `uniqueness` | A ratio that produces a number between 0 and 100 that indicates how unique the data in a column is.  0 indicates that all the values are the same; 100 indicates that all the values in the column are unique.  | duplicates |


In the example below, a Soda SQL scan runs two tests on the contents of the `id` column: 
- test for values that are not in UUID format
- test for duplicate values

Because the YAML file also defines `metric_groups: duplicates`, the scan also tests all other metrics in the `duplicates` group. Refer to table below.

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
    metric_groups:
    - duplicates
    valid_format: uuid
    tests:
      - invalid_percentage == 0
      - duplicate_count == 0
  feepct:
    valid_format: number_percentage
    tests:
      - invalid_percentage == 0
```

The example above defines metric groups at the **column level**, but you can also define metric groups at the **dataset level** so as to use the individual metrics from the group in tests in multiple columns. See example below.

```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
metric_groups:
  - duplicates
tests:
  - row_count > 0
columns:
  id:
    valid_format: uuid
    tests:
      - invalid_percentage == 0
      - duplicate_count == 0
  feepct:
    valid_format: number_percentage
    tests:
      - invalid_percentage == 0
      - duplicate_count == 0
```

By default, there exist **dependencies** between some metrics. If Soda SQL scans a metric which has dependencies, it includes all the dependent metrics in the scan as well.

| If you use... | ...the scan includes: |
| ------ | ------------ |
| `valid_count` | `missing_count` |
| `valid_percentage` | `missing_percentage` |
| `invalid_count` | `values_count` |
| `invalid_percentage`| `values_percentage`|
| `missing_count` <br /> `missing_percentage` <br /> `values_count` <br /> `values_percentage` | `row_count` |
| `histogram` | `min` <br /> `max` |



## Custom metrics

If the built-in set of dataset and column metrics that Soda SQL offers do not quite give you the information you need from a scan, you can use **custom metrics** to customize your queries. Custom metrics, also known as SQL metrics, essentially enable you to add SQL queries to your scan YAML file so that Soda SQL runs them during a scan.


#### Dataset custom metric example
In your scan YAML file, use the `sql_metrics` property as a dataset metric or a column metric. The following simple custom metric example queries all data in the dataset to select a single numeric value. The outcome of the test determines whether or not the volume of transactions in the United States is greater than 5000.

```yaml
table_name: mytable
sql_metrics:
    - sql: |
        SELECT sum(volume) as total_volume_us
        FROM CUSTOMER_TRANSACTIONS
        WHERE country = 'US'
      tests:
        - total_volume_us > 5000
```
In the example, the computed value (the sum volume of all customer transaction in the United States) becomes a **field** named `total_volume_us`, which, in turn, becomes the name of the metric that you use to define the test Soda SQL that runs on your data. In this case, the test passes if the computed sum of all US transactions exceeds `5000`.

Notice that by default, Soda SQL uses the name of the field as the name of the metric. If you do not want to use the default field names inside your SQL queries, you can explicitly name the metrics outside the queries. See [Custom metric names](#custom-metric-names) below.


#### Multiple example

You can also compute multiple metric values in a single query, then combine them in your tests.

```yaml
table_name: mytable
sql_metrics:
    - sql: |
        SELECT sum(volume) as total_volume_us,
               min(volume) as min_volume_us,
               max(volume) as max_volume_us
        FROM CUSTOMER_TRANSACTIONS
        WHERE country = 'US'
      tests:
        - total_volume_us > 5000
        - min_volume_us > 20
        - max_volume_us > 100
        - max_volume_us - min_volume_us < 60
```
In this example, the tests pass if:

- the computed sum of all US transactions exceeds `5000`
- the numerical value of the smallest of all US transactions is greater than `20`
- the numerical value of the greatest of all US transactions is greater than `100`
- the numerical value of the difference between the greatest and smallest of US transactions is less than `60`


#### Column custom metric example

The following example uses custom metrics to run a query against an individual column named `volume`. When you use custome metrics in a column, the field you define becomes available to use as a metric in the tests in that column.

```yaml
table_name: mytable
columns:
    metrics:
        - avg
    volume:
        sql_metrics:
            - sql: |
                SELECT sum(volume) as total_volume_us
                FROM CUSTOMER_TRANSACTIONS
                WHERE country = 'US'
              tests:
                - total_volume_us - avg > 5000
```


### Custom metric names

If you do not want to use the default field names inside your SQL queries, you can use the **`metric_names` property** to explicitly name the metrics outside the queries. This property contains a list of values which match the order of values in your `SELECT` statement.

```yaml
table_name: mytable
sql_metrics:
    - sql: |
        SELECT sum(volume),
               min(volume),
               max(volume)
        FROM CUSTOMER_TRANSACTIONS
        WHERE country = 'US'
      metric_names:
        - total_volume_us
        - min_volume_us
        - max_volume_us
      tests:
        - total_volume_us > 5000
        - min_volume_us > 20
        - max_volume_us > 100
        - max_volume_us - min_volume_us < 60
```


### GROUP BY queries in custom metrics

If your SQL query uses a `GROUP BY` clause, you can use a `group_fields` property in your custom metrics to instruct Soda SQL to run each test against each group combination. The example below runs each of the four tests against each country in the dataset.

```yaml
table_name: mytable
sql_metrics:
    - sql: |
        SELECT country,
               sum(volume) as total_volume,
               min(volume) as min_volume,
               max(volume) as max_volume
        FROM CUSTOMER_TRANSACTIONS
        GROUP BY country
      group_fields:
        - country
      tests:
        - total_volume > 5000
        - min_volume > 20
        - max_volume > 100
        - max_volume - min_volume < 60
```


### Variables in custom metrics

In Soda SQL, you set a **variable** to apply a filter to the data that Soda SQL scans. Often you use a variable to filter the range of a scan by date. Refer to [Apply filters](/docs/soda-sql/filtering.md) for details.

When you define a variable in your scan YAML file, Soda SQL applies the filter to all tests *except* tests defined in custom metrics. To apply a filter to custom metrics tests, be sure to explicitly define the variable in your SQL query, as in the example below.

```yaml
table_name: mytable
filter: date = DATE '{{ date }}'
sql_metrics:
    - sql: |
        SELECT sum(volume) as total_volume_us
        FROM CUSTOMER_TRANSACTIONS
        WHERE country = 'US' AND date = DATE '{{ date }}'
      tests:
        - total_volume_us > 5000
```


### Custom metrics using file reference

Instead of including all your customized SQL queries in the custom metrics in your scan YAML file, you can use **`sql_file`** to reference a relative file.

```yaml
table_name: mytable
sql_metrics:
    - sql_file: mytable_metric_us_volume.sql
      tests:
        - total_volume_us > 5000
```

In this case, the `mytable_metric_us_volume.sql` file contains the following SQL query.

```sql
SELECT sum(volume) as total_volume_us
FROM CUSTOMER_TRANSACTIONS
WHERE country = 'US'
```