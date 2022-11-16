# Example tests for unique values

Where your dataset contains records that ought to be unique, such as item identifiers, you may wish to test the data to ensure there are no duplicates or that each value is unique.  

To illustrate how to use Soda SQL to test the uniqueness of data, imagine an e-commerce company that fulfills orders for shipment to customers. The information associated with each shipment is stored in a fulfillment table in a database. Here are some of the ways the company could test their data.

## Test for duplicates

The company needs to make sure that each individual shipment is associated with a unique identifier for tracking purposes. To ensure that `shipment_id` is not accidentally duplicated in their fulfillment system, a Data Engineer could use Soda SQL to test for duplicates. To do so, the engineer defines a [metric group](/docs/soda-sql/sql_metrics.md#metric-groups-and-dependencies) and a test in the [scan YAML file](/docs/soda-sql/scan-yaml.md) associated with the table that contains the `shipment_id` data.

Scan YAML:

```yaml
table_name: fulfillment
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
metric_groups:
  - duplicates
columns:
  shipment_id:
    tests:
      - duplicate_count == 0
```

Then, the engineer [runs a Soda SQL scan](/docs/soda-sql/scan.md#run-a-scan-in-soda-sql) as follows:

Scan command:

`soda scan warehouse.yml tables/fulfillment.yml`

Scan output:

```bash
| 2.x.x
| Scanning tables/fulfillment.yml ...
| ...
| Test column(shipment_id) test(duplicate_count == 0) passed with metric values {"duplicate_count": 0}
| Executed 8 queries in 0:00:00.055843
| Scan summary ------
| 92 measurements computed
| 1 tests executed
| All is good. No tests failed.
| Exiting with code 0 
```

## Test for unique

Alternatively, to ensure that each value in the `shipment_id` column is unique relative to all other values in the column, a Data Engineer could define a test to count unique values. To do so, the engineer defines a metric grou pand a test in the scan YAML file associated with the table that contains the `shipment_id` data.

Scan YAML:

```yaml
table_name: fulfillment
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
metric_groups:
  - duplicates
columns:
  shipment_id:
    tests:
      - unique_count > 0
```

Then, the engineer runs a Soda SQL scan as follows:

Scan command:

```soda scan warehouse.yml tables/fulfillment.yml```

Scan output, pass:

```shell
  | 2.x.x
  | Scanning tables/fulfillment.yml ...
  | ...
  | Test column(shipment_id) test(unique_count > 0) passed with metric values {"unique_count": 65}
  | Executed 8 queries in 0:00:00.058411
  | Scan summary ------
  | 92 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
  ```

Scan output, fail:

```shell
  | 2.x.x
  | Scanning tables/fulfillment.yml ...
  | ...
  | Test column(shipment_id) test(unique_count > 0) failed with metric values {"unique_count": 5}
  | Executed 8 queries in 0:00:00.056029
  | Scan summary ------
  | 92 measurements computed
  | 1 tests executed
  | 1 of 1 tests failed:
  |   Test column(shipment_id) test(unique_count > 0) failed with metric values {"unique_count": 5}
  | Exiting with code 1
```


## Test for uniqueness

Where absolutely unique values is not a requirement, a Data Engineer may wish to test data in a table column for relative uniqueness. Uniqueness is a ratio that produces a number between 0 and 100 that indicates how unique the data in a column is:  0 indicates that all the values are the same; 100 indicates that all the values in the column are unique. 

For example, to loosely gauge the concentration of fulfillment orders destined for a particular country, an engineer defines a metric group and a test in the scan YAML file associated with the table that contains `destination` data. 

Scan YAML:

```yaml
table_name: fulfillment
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
metric_groups:
  - duplicates
columns:
  destination:
    tests:
      - uniqueness > 1
```

Scan command:

```soda scan warehouse.yml tables/fulfillment.yml```

Scan output:

```shell
  | 2.x.x
  | Scanning tables/fulfillment.yml ...
  | ...
  | Test column(destination) test(uniqueness > 1) passed with metric values {"uniqueness": 4.6875}
  | Executed 8 queries in 0:00:00.050244
  | Scan summary ------
  | 92 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
  ```

<br />