# Configure programmatic scans

To automate the search for "bad" data, you can use the **Soda SQL Python library** to programmatically execute scans.

Based on a set of conditions or a specific event schedule, you can instruct Soda SQL to automatically scan a data source for “bad” data. For example, you may wish to scan your data at several points along your data pipeline, perhaps when new data enters a data source, after it is transformed, and before it is exported to another data source.

You can save Soda SQL scan results anywhere in your system; the `scan_result` object contains all the scan result information.

### Basic scan

Execute a scan based on Soda SQL's default directory structure.

```python
scan_builder = ScanBuilder()
scan_builder.scan_yml_file = 'tables/my_table.yml'
# scan_builder automatically finds the warehouse.yml in the parent directory of the scan YAML file
# scan_builder.warehouse_yml_file = '../warehouse.yml'
scan = scan_builder.build()
scan_result = scan.execute()
if scan_result.has_test_failures():
    print('Scan has test failures, stop the pipeline')
```

### Scans using dicts

```python
from sodasql.scan.scan_builder import ScanBuilder
scan_builder_customers = ScanBuilder()
scan_builder_customers.warehouse_yml_file = 'warehouse.yml'
scan_builder_customers.scan_yml_dict = {
  "table_name": "customer",
  "metrics": ["row_count"],
  "sql_metrics": [
    {
        "metric_names": [
               "max_size"
        ],
        "sql": "SELECT max(size) from customer;"
    }
  ],
  "tests": [
        "max_size < 50"
  ]
}
scan_customers = scan_builder_customers.build()
scan_result_customers = scan_customers.execute()
print('Scan Result Customers: ' +str(scan_result_customers.is_passed()))
```
<br />

```python
scan_builder = ScanBuilder()
scan_builder.warehouse_yml_dict = {
    'name': 'my_warehouse_name',
    'connection': {
        'type': 'snowflake',
        ...
    }
}
scan_builder.scan_yml_dict = {
    ...
}
scan = scan_builder.build()
scan_result = scan.execute()
if scan_result.has_test_failures():
print('Scan has test failures, stop the pipeline')
```


### Scan using a lambda function

```python
from sodasql.scan.scan_builder import ScanBuilder
from sodasql.__version__ import SODA_SQL_VERSION


def lambda_handler(event, context):
    print(f'Lambda Handler: Soda SQL Version: {SODA_SQL_VERSION}')
    scan_builder = ScanBuilder()
    scan_builder.warehouse_yml_dict = {
        'name': 'lambda-demo',
        'connection': {
            'type': 'postgres',
            'host': 'env_var(POSTGRES_URL)',
            'port': '5432',
            'username': 'env_var(POSTGRES_USERNAME)',
            'password': 'env_var(POSTGRES_PASSWORD)',
            'database': 'postgres',
            'schema': 'public'
        },
        'soda_account': {
            'host': 'cloud.soda.io',
            'api_key_id': 'env_var(API_PUBLIC)',
            'api_key_secret': 'env_var(API_PRIVATE)',
        }
    }

    scan_builder.scan_yml_file = 'product.yml'
    scan = scan_builder.build()
    scan_result = scan.execute()

    print("Finished: Soda Scan")
    print(scan_result.to_json())
```
