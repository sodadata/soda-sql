# Example tests by metric

Refer to [Metrics](/docs/soda-sql/sql_metrics.md) for configuration details for Soda SQL.
Refer to [Scan YAML](/docs/soda-sql/scan-yaml.md#anatomy-of-the-scan-yaml-file) for details on the anatomy of a scan YAML file.

[avg](/docs/soda-sql/examples-by-metric.md#avg)
[avg-length](/docs/soda-sql/examples-by-metric.md#avg-length)
[distinct](/docs/soda-sql/examples-by-metric.md#distinct)
[duplicate_count](/docs/soda-sql/examples-by-metric.md#duplicate_count)
[frequent_values](/docs/soda-sql/examples-by-metric.md#frequent_values)
[histogram](/docs/soda-sql/examples-by-metric.md#histogram)
[invalid_count](/docs/soda-sql/examples-by-metric.md#invalid_count)
[invalid_percentage](/docs/soda-sql/examples-by-metric.md#invalid_percentage)
[max](/docs/soda-sql/examples-by-metric.md#max)
[max_length](/docs/soda-sql/examples-by-metric.md#max_length)
[maxs](/docs/soda-sql/examples-by-metric.md#maxs)
[min](/docs/soda-sql/examples-by-metric.md#min)
[min_length](/docs/soda-sql/examples-by-metric.md#min_length)
[mins](/docs/soda-sql/examples-by-metric.md#mins)
[missing_count](/docs/soda-sql/examples-by-metric.md#missing_count)
[missing_percentage](/docs/soda-sql/examples-by-metric.md#missing_percentage)
[row_count](/docs/soda-sql/examples-by-metric.md#row_count)
[schema](/docs/soda-sql/examples-by-metric.md#schema)
[stddev](/docs/soda-sql/examples-by-metric.md#stddev)
[sum](/docs/soda-sql/examples-by-metric.md#sum)
[unique_count](/docs/soda-sql/examples-by-metric.md#unique_count)
[uniqueness](/docs/soda-sql/examples-by-metric.md#uniqueness)
[valid_count](/docs/soda-sql/examples-by-metric.md#valid_count)
[valid_percentage](/docs/soda-sql/examples-by-metric.md#valid_percentage)
[values_count](/docs/soda-sql/examples-by-metric.md#values_count)
[values_percentage](/docs/soda-sql/examples-by-metric.md#values_percentage)
[variance](/docs/soda-sql/examples-by-metric.md#variance)

----

### avg

The calculated average of values in a numeric column.

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  size:
    tests:
      - avg > 100
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(size) test(avg > 100) passed with metric values {"avg": 5384.6}
  | Executed 2 queries in 0:00:00.027354
  | Scan summary ------
  | 40 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```


### avg_length

The average length of string values in a column.

Scan YAML
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  id:
    tests:
      - avg_length > 30
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(id) test(avg_length > 30) passed with metric values {"avg_length": 36.0}
  | Executed 2 queries in 0:00:00.034843
  | Scan summary ------
  | 68 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```


### distinct

The number of rows that contain distinct values, relative to the column. For example, where a column has values: `aaa`, `aaa`, `bbb`, `ccc`, it has three distinct values.

Use with `metric_groups: duplicates` at table or column level. See [Metric groups and dependencies](/docs/soda-sql/sql_metrics.md#metric-groups-and-dependencies).

Scan YAML:
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
columns:
  id:
    tests: 
      - distinct > 1
  size:
    tests:
      - distinct > 1
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
FROM group_by_value
  | SQL took 0:00:00.007346
  | Query measurement: distinct(id) = 65
  | Query measurement: unique_count(id) = 65
  | Derived measurement: duplicate_count(id) = 0
  | Derived measurement: uniqueness(id) = 100
  | ...
FROM group_by_value
  | SQL took 0:00:00.003017
  | Query measurement: distinct(size) = 65
  | Query measurement: unique_count(size) = 65
  | Derived measurement: duplicate_count(size) = 0
  | Derived measurement: uniqueness(size) = 100
  | Test column(id) test(distinct > 1) passed with metric values {"distinct": 65}
  | Test column(size) test(distinct > 1) passed with metric values {"distinct": 65}
  | Executed 8 queries in 0:00:00.056644
  | Scan summary ------
  | 88 measurements computed
  | 2 tests executed
  | All is good. No tests failed.
  | Exiting with code 0

```

### duplicate_count

The number of rows that contain duplicate values, relative to the column. Use with `metric_groups: duplicates` at table or column level. See [Metric groups and dependencies](/docs/soda-sql/sql_metrics.md#metric-groups-and-dependencies).

Scan YAML:
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
columns:
  id:
    tests: 
      - duplicate_count == 0
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
FROM group_by_value
  | SQL took 0:00:00.002620
  | Query measurement: distinct(id) = 65
  | Query measurement: unique_count(id) = 65
  | Derived measurement: duplicate_count(id) = 0
  | Derived measurement: uniqueness(id) = 100
  | ...
  | Test column(id) test(duplicate_count == 0) passed with metric values {"duplicate_count": 0}
  | Executed 8 queries in 0:00:00.047606
  | Scan summary ------
  | 88 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

### frequent_values

A list of values in the column and the frequency with which they occur. Use with `metric_groups: profiling` at table or column level. See [Metric groups and dependencies](/docs/soda-sql/sql_metrics.md#metric-groups-and-dependencies).

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
metric_groups:
  - profiling
columns:
  size:
    tests:
      - frequent_values
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(size) test(frequent_values) passed with metric values {"frequent_values": [{"value": 6434, "frequency": 1}, {"value": 6210, "frequency": 1}, {"value": 3804, "frequency": 1}, {"value": 6383, "frequency": 1}, {"value": 6207, "frequency": 1}]}
  | Executed 16 queries in 0:00:00.082814
  | Scan summary ------
  | 54 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```


### histogram

A list of values to use to create a histogram that represents the contents of the column. Use with `metric_groups: profiling` at table or column level. See [Metric groups and dependencies](/docs/soda-sql/sql_metrics.md#metric-groups-and-dependencies).

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
metric_groups:
  - profiling
columns:
  size:
    tests:
      - histogram
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(size) test(histogram) passed with metric values {"histogram": {"boundaries": [1197.0, 1636.4, 2075.8, 2515.2, 2954.6, 3394.0, 3833.4, 4272.8, 4712.2, 5151.6, 5591.0, 6030.4, 6469.8, 6909.2, 7348.6, 7788.0, 8227.4, 8666.8, 9106.2, 9545.6, 9985.0], "frequencies": [5, 2, 5, 2, 3, 5, 4, 2, 2, 1, 3, 7, 5, 5, 2, 3, 1, 0, 4, 4]}}
  | Executed 16 queries in 0:00:00.075220
  | Scan summary ------
  | 54 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```


### invalid_count

The number of rows that contain invalid values.

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  id:
    valid_format: uuid
    tests:
      - invalid_count == 0
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(id) test(invalid_count == 0) passed with metric values {"invalid_count": 0}
  | Executed 2 queries in 0:00:00.027116
  | Scan summary ------
  | 44 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

### invalid_percentage

The percentage of rows that contain invalid values.

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  feepct:
    valid_format: number_percentage
    tests:
      - invalid_percentage == 0
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(feepct) test(invalid_percentage == 0) passed with metric values {"invalid_percentage": 0.0}
  | Executed 2 queries in 0:00:00.031899
  | Scan summary ------
  | 50 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

Scan YAML:
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
  country:
    valid_values:
      - US
      - UK
      - Netherlands
    tests:
      - invalid_percentage == 0
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test test(row_count > 0) passed with metric values {"row_count": 65}
  | Test column(country) test(invalid_percentage == 0) failed with metric values {"invalid_percentage": 10.76923076923077}
  | Executed 2 queries in 0:00:00.040941
  | Scan summary ------
  | 68 measurements computed
  | 2 tests executed
  | 1 of 2 tests failed:
  |   Test column(country) test(invalid_percentage == 0) failed with metric values {"invalid_percentage": 10.76923076923077}
  | Exiting with code 1
```

### max

The greatest value in a numeric column.

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  size:
    tests:
      - max > 100
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(size) test(max > 100) passed with metric values {"max": 9985}
  | Executed 2 queries in 0:00:00.028452
  | Scan summary ------
  | 40 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  size:
    tests:
      - max
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(size) test(max) passed with metric values {"max": 9985}
  | Executed 2 queries in 0:00:00.027402
  | Scan summary ------
  | 40 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```


### max_length

The maximum length of string values in a column.

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  country:
    tests:
      - max_length
  id:
    tests:
      - max_length
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(id) test(max_length) passed with metric values {"max_length": 36}
  | Test column(country) test(max_length) passed with metric values {"max_length": 11}
  | Executed 2 queries in 0:00:00.029349
  | Scan summary ------
  | 40 measurements computed
  | 2 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```



### maxs

A list of the five values that qualify as maximum relative to other values in the column. In other words, this metric returns the five greatest values in the column. 

Use with `metric_groups: profiling` at table or column level. See [Metric groups and dependencies](/docs/soda-sql/sql_metrics.md#metric-groups-and-dependencies).

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
metric_groups:
  - profiling
columns:
  size:
    tests:
      - maxs
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(size) test(maxs) passed with metric values {"maxs": [9985, 9932, 9685, 9664, 9427]}
  | Executed 16 queries in 0:00:00.071264
  | Scan summary ------
  | 54 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```



### min

The smallest value in a numeric column.

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  size:
    tests:
      - min > 50
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(size) test(min > 50) passed with metric values {"min": 1197}
  | Executed 2 queries in 0:00:00.030317
  | Scan summary ------
  | 40 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  size:
    tests:
      - min
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(size) test(min) passed with metric values {"min": 1197}
  | Executed 2 queries in 0:00:00.026789
  | Scan summary ------
  | 40 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```


### min_length

The minimum length of string values in a column.

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  country:
    tests:
      - min_length
  id:
    tests:
      - min_length
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(id) test(min_length) passed with metric values {"min_length": 36}
  | Test column(country) test(min_length) passed with metric values {"min_length": 2}
  | Executed 2 queries in 0:00:00.028297
  | Scan summary ------
  | 40 measurements computed
  | 2 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```


### mins

A list of the five values that qualify as minimum relative to other values in the column. In other words, this metric returns the five smallest values in the column.

Use with `metric_groups: profiling` at table or column level. See [Metric groups and dependencies](/docs/soda-sql/sql_metrics.md#metric-groups-and-dependencies).

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
metric_groups:
  - profiling
columns:
  size:
    tests:
      - mins
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(size) test(mins) passed with metric values {"mins": [1197, 1277, 1304, 1442, 1531]}
  | Executed 16 queries in 0:00:00.084354
  | Scan summary ------
  | 54 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```


### missing_count

The number of rows in a column that do not contain specific content.

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  id:
    valid_format: uuid
    tests:
      - missing_count == 0
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(id) test(missing_count == 0) passed with metric values {"missing_count": 0}
  | Executed 2 queries in 0:00:00.030209
  | Scan summary ------
  | 44 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

Scan YAML, where `country` column contains valid value `US`:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - values_percentage
  - valid_count
  - ...
columns:
  country:
    missing_values: 
    - US
    tests:
      - missing_count == 0
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(country) test(missing_count == 0) failed with metric values {"missing_count": 35}
  | Executed 2 queries in 0:00:00.035223
  | Scan summary ------
  | 68 measurements computed
  | 1 tests executed
  | 1 of 1 tests failed:
  |   Test column(country) test(missing_count == 0) failed with metric values {"missing_count": 35}
  | Exiting with code 1
```

### missing_percentage

The percentage of rows in a column that do not contain specific content.

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  id:
    valid_format: uuid
    tests:
      - missing_percentage < 1
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(id) test(missing_percentage < 1) passed with metric values {"missing_percentage": 0.0}
  | Executed 2 queries in 0:00:00.034878
  | Scan summary ------
  | 44 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

### row_count

The number of rows in a table or column.

Scan YAML, row_count at table level:
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
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test test(row_count > 0) passed with metric values {"row_count": 65}
  | Executed 2 queries in 0:00:00.034396
  | Scan summary ------
  | 40 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

Scan YAML, row_count at column level:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  size:
    tests:
      - row_count > 0
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test test(row_count > 0) passed with metric values {"row_count": 65}
  | Executed 2 queries in 0:00:00.034396
  | Scan summary ------
  | 40 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

Scan YAML, row_count at column level:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  size:
    tests:
      - row_count
```

Scan output:
```shell
  | Test column(size) test(row_count) passed with metric values {"row_count": 65}
  | Executed 2 queries in 0:00:00.025365
  | Scan summary ------
  | 40 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

### schema

A list of column names in a table, and their data types.

Scan YAML, at table level:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
tests:
  - schema
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test test(schema) passed with metric values {"schema": [{"name": "id", "type": "character varying"}, {"name": "name", "type": "character varying"}, {"name": "size", "type": "integer"}, {"name": "date", "type": "date"}, {"name": "feepct", "type": "character varying"}, {"name": "country", "type": "character varying"}]}
  | Executed 2 queries in 0:00:00.026430
  | Scan summary ------
  | 40 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```



### stddev

The calculated standard deviation of values in a numeric column. 

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  size:
    tests:
      - stddev > 1000
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(size) test(stddev > 1000) passed with metric values {"stddev": 2541.94966880739}
  | Executed 2 queries in 0:00:00.027737
  | Scan summary ------
  | 40 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  size:
    tests:
      - stddev
```

Scan output:
```shell
  | Test column(size) test(stddev) passed with metric values {"stddev": 2541.94966880739}
  | Executed 2 queries in 0:00:00.024660
  | Scan summary ------
  | 40 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

### sum

The calculated sum of the values in a numeric column. 

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  size:
    tests:
      - sum > 300000
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(size) test(sum > 300000) passed with metric values {"sum": 349999}
  | Executed 2 queries in 0:00:00.027154
  | Scan summary ------
  | 40 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```


Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  size:
    tests:
      - sum
```

Scan output:
```shell
  | Test column(size) test(sum) passed with metric values {"sum": 349999}
  | Executed 2 queries in 0:00:00.030573
  | Scan summary ------
  | 40 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

### unique_count

The number of rows in which a value appears exactly only once in the column. For example, where a column has values: `aaa`, `aaa`, `bbb`, `ccc`, it has two unique values.

Use with `metric_groups: duplicates` at table or column level. See [Metric groups and dependencies](/docs/soda-sql/sql_metrics.md#metric-groups-and-dependencies).

Scan YAML:
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
columns:
  id:
    tests: 
      - unique_count > 0
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
FROM group_by_value
  | SQL took 0:00:00.003185
  | Query measurement: distinct(id) = 65
  | Query measurement: unique_count(id) = 65
  | Derived measurement: duplicate_count(id) = 0
  | Derived measurement: uniqueness(id) = 100
  | ...
  | Test column(id) test(unique_count > 0) passed with metric values {"unique_count": 65}
  | Executed 8 queries in 0:00:00.054074
  | Scan summary ------
  | 88 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

### uniqueness

A ratio that produces a number between 0 and 100 that indicates how unique the data in a column is.  0 indicates that all the values are the same; 100 indicates that all the values in the the column are unique. Use with `metric_groups: duplicates` at table or column level. See [Metric groups and dependencies](/docs/soda-sql/sql_metrics.md#metric-groups-and-dependencies).

Scan YAML:
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
columns:
  id:
    tests: 
      - uniqueness == 100
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
FROM group_by_value
  | SQL took 0:00:00.002458
  | Query measurement: distinct(id) = 65
  | Query measurement: unique_count(id) = 65
  | Derived measurement: duplicate_count(id) = 0
  | Derived measurement: uniqueness(id) = 100
  | ...
  | Test column(id) test(uniqueness == 100) passed with metric values {"uniqueness": 100.0}
  | Executed 8 queries in 0:00:00.049126
  | Scan summary ------
  | 88 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```


### valid_count

The number of rows that contain valid content.

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  id:
    valid_format: uuid
    tests:
      - valid_count > 10
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(id) test(valid_count > 10) passed with metric values {"valid_count": 65}
  | Executed 2 queries in 0:00:00.030024
  | Scan summary ------
  | 44 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

### valid_percentage

The percentage of rows that contain valid content.

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  id:
    valid_format: uuid
    tests:
      - valid_percentage == 100
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(id) test(valid_percentage == 100) passed with metric values {"valid_percentage": 100.0}
  | Executed 2 queries in 0:00:00.033056
  | Scan summary ------
  | 44 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  country:
    valid_min_length: 10
    tests:
      - valid_percentage == 100
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(country) test(valid_percentage == 100) failed with metric values {"valid_percentage": 4.615384615384615}
  | Executed 2 queries in 0:00:00.029359
  | Scan summary ------
  | 68 measurements computed
  | 1 tests executed
  | 1 of 1 tests failed:
  |   Test column(country) test(valid_percentage == 100) failed with metric values {"valid_percentage": 4.615384615384615}
  | Exiting with code 1
```


### values_count

The number of rows that contain content included in a list of valid values.

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  country:
    valid_values: 
      - US
      - UK
    tests:
      - values_count > 1
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(country) test(values_count > 1) passed with metric values {"values_count": 65}
  | Executed 2 queries in 0:00:00.032684
  | Scan summary ------
  | 44 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

### values_percentage

The number of rows that contain content included in a list of valid values.

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  country:
    valid_values: 
      - US
      - UK
    tests:
      - values_percentage > 10
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(country) test(values_percentage > 10) passed with metric values {"values_percentage": 100.0}
  | Executed 2 queries in 0:00:00.027640
  | Scan summary ------
  | 44 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0

```

### variance

The calculated variance of the values in a numeric column.

Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  size:
    tests:
      - variance > 0
```

Scan output:
```shell
  | 2.x.x
  | Scanning tables/demodata.yml ...
  | ...
  | Test column(size) test(variance > 0) passed with metric values {"variance": 6461508.11875}
  | Executed 2 queries in 0:00:00.046971
  | Scan summary ------
  | 40 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```


Scan YAML:
```yaml
table_name: demodata
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  size:
    tests:
      - variance
```

Scan output:
```shell
  | Test column(size) test(variance) passed with metric values {"variance": 6461508.11875}
  | Executed 2 queries in 0:00:00.030379
  | Scan summary ------
  | 40 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```
