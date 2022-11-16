<br />

![soda-sql-logo](/docs/assets/images/soda-sql-logo.png)
<br />

&#10004;  <a href="https://github.com/sodadata/soda-sql" target="_blank">Open-source software</a><br />

&#10004;  [Install](/docs/soda-sql/installation.md) from the command-line <br />

&#10004;  Compatible with Snowflake, Amazon Redshift, BigQuery, [and more](/docs//soda-sql/installation.md#compatibility)<br />

&#10004; [Write tests](/docs/soda-sql/tests.md) in a YAML file<br />

&#10004;  Deploy in an [Airflow enviroment](/docs/soda-sql/orchestrate_scans.md)<br />
<br />

#### Example scan YAML file
```yaml
table_name: breakdowns
metrics:
  - row_count
  - missing_count
  - missing_percentage
...
# Validates that a table has rows
tests:
  - row_count > 0

# Tests that numbers in the column are entered in a valid format as whole numbers
columns:
  incident_number:
    valid_format: number_whole
    tests:
      - invalid_percentage == 0

# Tests that no values in the column are missing
  school_year:
    tests:
      - missing_count == 0

# Tests for duplicates in a column
  bus_no:
    tests:
      - duplicate_count == 0

# Compares row count between datasets
sql_metric: 
  sql: |
    SELECT COUNT(*) as other_row_count
    FROM other_table
  tests:
    - row_count == other_row_count
```

## Get started
* <a href="https://github.com/sodadata/tutorial-demo-project" target="_blank">Soda SQL playground in GitHub</a>
* [Install Soda SQL](/docs/soda-sql/installation.md)
* [Quick start for Soda SQL and Soda Cloud](/docs/soda-sql/quick-start-soda-sql.md)
