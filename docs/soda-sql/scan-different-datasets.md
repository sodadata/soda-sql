# Scan multiple data sources or datasets

You can run a single scan against different data sources in your environments. For example, you can run the same scan against data in a development environment and data in a production environment.

You can also run a single scan against different datasets in your data source using custom metrics. 

## Run a basic scan

When you run a scan, Soda SQL uses the configurations in your [scan YAML file](/docs/soda-sql/scan-yaml.md) and Soda Cloud monitors to prepare, then run SQL queries against data in your data source. The default tests and metrics Soda SQL configured when it created the YAML file focus on finding missing, invalid, or unexpected data in your datasets.

Each scan requires the following as input:
- a warehouse YAML file, which represents a connection to your data source
- a scan YAML file, including its filepath, which contains the metric and test instructions that Soda SQL uses to scan datasets in your data source

#### Example command 
```shell
$ soda scan warehouse.yml tables/demodata.yml
```

## Scan multiple data sources

To run the same scan against different data sources, proceed as follows.

1. Prepare one [warehouse YAML file](/docs/soda-sql/warehouse.md) for each data source you wish to scan. For example:
* `warehouse_postgres_dev.yml`
```yaml
name: my_postgres_datawarehouse_dev
connection:
  type: postgres
  host: localhost
  port: '5432'
  username: env_var(POSTGRES_USERNAME)
  password: env_var(POSTGRES_PASSWORD)
  database: dev
  schema: public
```
* `warehouse_postgres_prod.yml`
```yaml
name: my_postgres_datawarehouse_prod
connection:
  type: postgres
  host: dbhost.example.com
  port: '5432'
  username: env_var(POSTGRES_USERNAME)
  password: env_var(POSTGRES_PASSWORD)
  database: prod
  schema: public
```
2. Prepare a [scan YAML file](/docs/soda-sql/scan-yaml.md) to define all the tests you wish to run against your data sources. See [Define tests](/docs/soda-sql/tests.md) for details.
3. Run separate Soda SQL scans against each data source by specifying which warehouse YAML to scan and using the same scan YAML file. For example:
```shell
soda scan warehouse_postgres_dev.yml tables/my_dataset_scan.yml 
soda scan warehouse_postgres_prod.yml tables/my_dataset_scan.yml
```

## Scan multiple datasets

Use a single scan YAML file to run tests on different datasets in your data source.

Prepare one [scan YAML file](/docs/soda-sql/scan-yaml.md) to define the tests you wish to apply against multiple datasets. Use custom metrics to write SQL queries and subqueries that run against multiple datasets. When you run a scan, Soda SQL uses your SQL queries to query data in the datasets you specified in your scan YAML file. 
