# Example tests for valid values

Where your dataset contains records that ought to contain only values that qualify as valid, you can use Soda SQL to test for data validity. 

To illustrate how to use Soda SQL to test for validity, imagine an e-commerce company that fulfills orders for shipment to customers. The information associated with each shipment is stored in a fulfillment table in a database. Here is how they could test to ensure the values in the `country` column are countries they ship to. This example uses the `valid_values` [column configuration key](/docs/soda-sql/sql_metrics.md#column-configuration-keys) to define a list of valid countries.

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
    valid_values:
      - US
      - UK
      - CN
    tests:
      - invalid_percentage == 0
```

Then, the engineer [runs a Soda SQL scan](/docs/soda-sql/scan.md#run-a-scan-in-soda-sql) as follows:

Scan command:

`soda scan warehouse.yml tables/fulfillment.yml`

Scan output, pass:

```
  | 2.x.x
  | Scanning tables/fulfillment.yml ...
  | ...
  | Test column(country) test(invalid_percentage == 0) passed with metric values {"invalid_percentage": 0}
  | Executed 2 queries in 0:00:00.029831
  | Scan summary ------
  | 68 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```

Scan output, fail:

```shell
  | 2.x.x
  | Scanning tables/fulfillment.yml ...
  | ...
  | Test column(country) test(invalid_percentage == 0) failed with metric values {"invalid_percentage": 10.76923076923077}
  | Executed 2 queries in 0:00:00.053734
  | Scan summary ------
  | 68 measurements computed
  | 1 tests executed
  | 1 of 1 tests failed:
  |   Test column(country) test(invalid_percentage == 0) failed with metric values {"invalid_percentage": 10.76923076923077}
  | Exiting with code 1
```

<br />
<br />

Another way to test data for validity is to use the `valid_format` column configuration key. The data engineer can identify valid data using the `valid_format` column configuration key on the text column that contains customer_id values. The test ensures that all customer identifiers are in `uuid` format. (Note that `valid_format` only works with columns using [data type](/docs/soda-sql/supported-data-types.md) TEXT, *not* date or number.)

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
  customer_id:
    valid_format: uuid
    tests:
      - valid_percentage == 100
```

Then, the engineer [runs a Soda SQL scan](/docs/soda-sql/scan.md#run-a-scan-in-soda-sql) as follows:

Scan command:

`soda scan warehouse.yml tables/fulfillment.yml`

Scan output:

```
  | 2.x.x
  | Scanning tables/fulfillment.yml ...
  | ...
  | Test column(customer_id) test(valid_percentage == 100) passed with metric values {"valid_percentage": 100.0}
  | Executed 2 queries in 0:00:00.032870
  | Scan summary ------
  | 68 measurements computed
  | 1 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
```