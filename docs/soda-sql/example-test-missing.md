# Example tests for missing values

Where your dataset contains records that ought not to be empty, you can use Soda SQL to test for missing data, or null values. By default, Soda SQL includes a `missing_count` metric that searches for missing or null values in a column of a dataset. 

To illustrate how to use Soda SQL to test for missing values, imagine an e-commerce company that fulfills orders for shipment to customers. The information associated with each shipment is stored in a fulfillment table in a database. Here is how they could test to ensure the values in the `postal_code` column are not blank.

Scan YAML:

```yaml
table_name: fulfillment
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  postal_code:
    tests:
      - missing_count == 0
```

Then, the engineer [runs a Soda SQL scan](/docs/soda-sql/scan.md#run-a-scan-in-soda-sql) as follows:

Scan command:

```soda scan warehouse.yml tables/fulfillment.yml```

Scan output:

```shell
  | 2.x.x
  | Scanning tables/fulfillment.yml ...
  | ...
  | Test column(postal_code) test(missing_count == 0) passed with metric values {"missing_count": 0}
  | Executed 2 queries in 0:00:00.032096
  | Scan summary ------
  | 68 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

<br />
<br />

Another way to use the `missing_count` metric is to test for specific values that qualify as missing. For example, where "n/a" qualifies as a missing value in an unvalidated text field for `country` for a shipment, an engineer can define a Soda SQL test that looks for those missing values using a [column configuration key](/docs/soda-sql/sql_metrics.md#column-configuration-keys). 

Scan YAML:

```yaml
table_name: fulfillment
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
columns:
  country:
    missing_values:
    - n/a
    - na
    tests:
      - missing_count == 0
```

Then, the engineer [runs a Soda SQL scan](/docs/soda-sql/scan.md#run-a-scan-in-soda-sql) as follows:

Scan command:

```soda scan warehouse.yml tables/fulfillment.yml```

Scan output, pass:

```shell
  | 2.x.x
  | Scanning tables/fulfillment.yml ...
  | ...
  | Test column(country) test(missing_count == 0) passed with metric values {"missing_count": 0}
  | Executed 2 queries in 0:00:00.036880
  | Scan summary ------
  | 68 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

Scan output, fail:

```
  | 2.x.x
  | Scanning tables/fulfillment.yml ...
  | ...
  | Test column(country) test(missing_count == 0) failed with metric values {"missing_count": 35}
  | Executed 2 queries in 0:00:00.031306
  | Scan summary ------
  | 68 measurements computed
  | 1 tests executed
  | 1 of 1 tests failed:
  |   Test column(country) test(missing_count == 0) failed with metric values {"missing_count": 35}
  | Exiting with code 1
```
