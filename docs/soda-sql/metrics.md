# Metrics in Soda SQL

A **metric** is a property of the data in your database. A **measurement** is the value for a metric that Soda checks against during a scan. You use metrics to define the tests that Soda executes against your data during a scan. 

For example, in the test defined as `row_count > 0`, `row_count` is the metric and `0` is the measurement. When it runs a scan, Soda executes the test against your dataset; if the row count is greater than `0`, the test passes; if the dataset is empty, the test fails.

* In **Soda SQL**, you use metrics to define tests in your scan YAML file. Read more about [configuring metrics](/docs/soda-sql/sql_metrics.md). 
* In **Soda Cloud**, you use metrics to define a test as part of the process to create a new monitor. 

There are four kinds of metrics Soda uses:

* **[Dataset metrics](#dataset-metrics)** for tests that execute against an entire dataset
* **[Column metrics](#column-metrics)** for tests that execute against an individual column
* **[Custom metrics](#custom-metrics)**, also known as SQL metrics, enable you to define your own metric that you can use tests that execute against a dataset or a column; you can also use custom metrics to simply define SQL queries that Soda executes during a scan
* **[Historic metrics](#historic-metrics)** for tests that rely on historic measurements stored in the Cloud Metric Store

## Dataset metrics

Use **dataset metrics** in tests that execute against all data in the dataset during a scan. 

| Dataset metric <br />in Soda SQL |Dataset metric <br />in Soda Cloud | Description      |
| ---------- | ---------------- | -------------|
| `row_count` | Row Count  |The number of rows in a dataset. |
| `schema` | n/a | A list of column names in a dataset, and their data types. |

## Column metrics

Use **column metrics** in tests that execute against specific columns in a dataset during a scan.

Where a column metric references a valid or invalid value, or a limit, use the metric in conjunction with a **column configuration key** in Soda SQL or a **Validity Rule** in Soda Cloud. A Soda scan uses the value of a column configuration key / validity rule to determine if it should pass or fail a test.

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

### Column configuration keys or validity rules

Refer to [Using regex with column metrics](#using-regex-with-column-metrics) for important details on how to define the regex in a YAML file. The column configuration key:value pair defines what Soda SQL ought to consider as "valid" or "missing".

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



## Custom metrics

If the built-in dataset and column metrics that Soda offers do not quite give you the information you need from a scan, you can use **custom metrics** to customize your queries. Custom metrics, also known as SQL metrics, essentially enable you to define SQL queries that Soda runs during a scan. You can also use custom metrics to define new metrics that you can use when you write tests. See [Validate that row counts are equal](/docs/soda-sql/custom-metric-templates.md#validate-that-row-counts-are-equal) for an example of a test that uses a custom metric.

Read more about using [custom metrics in Soda SQL](/docs/soda-sql/sql_metrics.md#custom-metrics).

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