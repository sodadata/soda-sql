# Send failed row samples to Soda Cloud

When a scan results in a failed test, the CLI output displays information about the test that failed and why.  To offer more insight into the data that failed a test, [Soda Cloud](/docs/soda-cloud/soda-cloud-architecture.md) displays **failed rows** in a monitor's history. 

There are three ways you can configure Soda SQL to send failed row samples to your Soda Cloud account:

1. define a [samples configuration key](#define-a-samples-configuration-key-to-send-failed-rows) in your scan YAML file
2. use a [missing-value Metric Type](#use-a-missing-value-metric-type-to-send-failed-row-samples) in your monitor in Soda Cloud
3. use custom metrics in your scan YAML file to [explicitly send `failed_rows`](#explicitly-send-a-sample-of-failed-rows) 

For security, you can also [disable the failed row samples](#disable-failed-row-samples) feature, or [reroute failed row samples for a dataset](#reroute-failed-row-samples-for-a-dataset) to an alternate location.

## Define a samples configuration key to send failed rows

1. If you have not already done so, [connect Soda SQL to your Soda Cloud account](/docs/soda-sql/connect_to_cloud.md).
2. Define a `samples` configuration key in your scan YAML file according to the Scan YAML example below; use `failed_limit` to define a value that represents the numerical threshold of rows in a dataset that Soda SQL sends to Soda Cloud as a sample of failed rows for any tests that fail during a scan. A sample contains the first *n* number of rows from the dataset, according to the limit you specify.

For this example, imagine you define a test in your scan YAML file to make sure that 99% of the values in the `productid` column are correctly formatted as universally unique identifiers (UUID), then you [run a scan](/docs/soda-sql/scan.md#run-a-scan-in-soda-sql) from the command line to execute the test on the data in your dataset.

#### Scan YAML Example

```yaml
table_name: orders
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - ...
samples:
  failed_limit: 50
tests:
  - row_count > 0
columns:
  productid:
    valid_format: uuid
    tests:
      - invalid_percentage <= 1
```

CLI output:
```shell
  | Scan summary ------
  | 126 measurements computed
  | 2 tests executed
  | 1 of 2 tests failed:
  |   Test column(productid) test(invalid_percentage <= 1) failed with measurements {"invalid_percentage": 5.181347150259067}
  | Exiting with code 1
```

The scan results in a failed test that indicates that 5.18% of the rows in the `productid` column are incorrectly formatted. This is all the information that the CLI output reveals. To review the data that failed the test, you must directly access the dataset in the data source. However, if you are a Soda Cloud user, you can review the data in the failed rows without directly accessing the data.

In Soda Cloud, the Soda SQL test manifests as a line item in the **Monitor results** page. The line item reveals that the test failed with an invalid percentage value of 5.18, which is what Soda SQL CLI output revealed, but you can open the monitor and navigate to the **Failed Rows** tab to examine the contents of a sample of the rows that failed. Soda Cloud offers this quick view of the failing data in your dataset to help you identify issues and address causes.

![failed-rows](/docs/assets/images/failed-rows.png)

#### Troubleshoot

**Problem:** You open the monitor whose test failed during a scan but cannot click the **Failed Rows** tab. <br />
**Solution:** Click a failed data point in the chart that shows the monitor's scan results over time. This action identifies the specific set of failed rows associated with an individual scan result so it can display the failed rows associated with that individual scan. 

## Use a missing-value Metric Type to send failed row samples

If you use one of the following **Metric Types** in a test that you define in a monitor, Soda SQL automatically sends a sample of the first five failed rows associated with the failed test to Soda Cloud with the scan results. 

* Missing Values
* Invalid Values
* Distinct

When Soda Cloud runs its next scheduled scan of your dataset, or when you run a scan in Soda SQL, Soda SQL collects and sends a sample of failed rows for the monitors that use the above-listed metric types.

## Explicitly send a sample of failed rows

You can use Soda SQL [custom metrics](/docs/soda-sql/sql_metrics.md#custom-metrics) (also known as SQL metrics) to explicitly demand that Soda SQL send failed rows to Soda Cloud when a scan results in a failed test.

1. If you have not already done so, [connect Soda SQL to your Soda Cloud account](/docs/soda-sql/connect_to_cloud.md).
2. In your scan YAML file, use `type: failed_rows` when writing a SQL query to retrieve a sample of `failed_rows` in a dataset, as in the example below. By default, `failed_rows` collects five rows of data that failed the test defined in the SQL query and displays them in Soda Cloud as failed rows in the monitor that represents the test that failed during a scan. 

In the following example, Soda SQL runs the scan and Soda Cloud displays a sample of the first five `failed_rows` of data that failed the test defined as a SQL query.

```yaml
sql_metrics:
  - type: failed_rows
    name: PURCHASEPRICE_EXCEEDS_SELLINGPRICE
    sql: |
      SELECT *
      FROM ORDERS
      WHERE PURCHASEPRICE > SELLINGPRICE
```

## Disable failed row samples

Where your datasets contain sensitive or private information, you may *not* want to send failed row samples from your data source to Soda Cloud. In such a circumstance, you can disable the feature completely in Soda Cloud.

To prevent Soda Cloud from receiving any sample data or failed row samples for any datasets in any data sources to which you have connected your Soda Cloud account, proceed as follows:

1. As an Admin, log in to your Soda Cloud account and navigate to **your avatar** > **Organization Settings**.
2. In the **Organization** tab, check the box to "Disable storage of sample data and failed row samples in Soda Cloud.", then **Save**. 

Alternatively, you can prevent Soda SQL from sending metadata or samples to Soda Cloud by using one of the following methods:
* To prevent Soda SQL from sending an individual dataset's scan results or samples to Soda Cloud, use the [`--offline` option](/docs/soda-sql/scan.md#add-scan-options) when you run a scan.
* To prevent Soda SQL from sending specific column scan results or samples, configure an [`excluded_columns` configuration key](/docs/soda-sql/scan-yaml.md#scan-yaml-table-configuration-keys) in your scan YAML file.

## Reroute failed row samples for a dataset 

Use a `FailedRowsProcessor` to send a dataset's failed row samples to a secure location within your organization's infrastructure, such as an Amazon S3 bucket or Google Big Query. In Soda Cloud, users looking for failed row samples see the message you define advising them where they can access and review failed row samples for the dataset.

![failed-row-message](/docs/assets/images/failed-row-message.png)


#### Reroute to Amazon S3

Note that you can only configure failed row sample rerouting for individual datasets, and only for those scans that you have scheduled programmatically. 

First, configure the `FailedRowProcessor` according to the following example.

```python
import boto
import json

from soda.scan.FailedRowsProcessor

class S3FailedRowProcessor(FailedRowsProcessor):
  # Override the process function
  def process(context) → dict:
    file_name = 'failed_rows.json'
    with open(file_name, 'w', encoding='uft-8') as f:
      json.dump(, f)

    s3_client = boto3.client('s3')
    if object_name is None:
      object_name = os.path.basename(file_name)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return {'message': 'Unable to load failed rows into S3'}
    return {'message':
             f'Failed rows are saved to s3://{bucket_name}/{file_name}'}
```

Then, configure the failed row processor in a scan builder as per the example below.
```python
scan_builder.failed_row_processor = S3FailedRowProcessor()
scan_result = scan_builder.build().execute()
```
<br />

#### Reroute to Google Big Query using existing credentials

Note that you can only configure failed row sample rerouting for individual datasets, and only for those scans that you have [scheduled programmatically](/docs/soda-sql/programmatic_scan.md). 

This configuration uses the Big Query access credentials that Soda SQL uses. These credentials must have the appropriate service account and scopes in Big Query which give Soda SQL write permission on the table. 

First, configure a `FailedRowProcessor` according to the following example. Note that the `client` parameter points to different objects for different warehouses.
```python
import bigquery
from soda.scan.FailedRowsProcessor

class BigQueryFailedRowProcessor(FailedRowsProcessor):
  # Override process function - conn/context
  # (here only treating it as a bigquery client)
  def process(context) → dict:
    table_id = "your-project.your_dataset.your_table"

    errors = conn.insert_rows_json(
        table_id, rows, row_ids=[None] * len(rows_to_insert)
    )  # Make an API request.
    if errors == []:
        return { 'count': 50,
                'columns': ['id', 'amount']
                 'message': f'Faled rows saved to {table_id}'}
    else:
       return {'message': 'Unable to save failed rows to Bigquery'}
```
Then, configure the failed row processor in a scan builder as per the example below.
```python
# scan_builder construction
scan_builder = ScanBuilder()
scan_builder.failed_row_processor = BigQueryRowProcessor()
```
<br />

#### Reroute to Google Big Query using separate credentials

This configuration *does not* use the Big Query access credentials that Soda SQL uses. The separate credentials must have the appropriate service account and scopes in Big Query which give Soda SQL write permission on the table. 

First, configure a `FailedProcessor` according to the following example. Note that the `client` parameter points to different objects for different warehouses.
```python
import json
import bigquery
from soda.scan.FailedRowsProcessor

class BigQueryFailedRowProcessor(FailedRowsProcessor):
  # Override process function
  # context: sql, connection, sample_reference
  def process(context) → dict:

    table_schema = {
     ## Define Schema for the failed rows dataset.table
    }

    project_id = '<my_project>'
    dataset_id = '<my_dataset>'
    table_id = '<my_table>'

    client  = bigquery.Client(project = project_id)
    dataset  = client.dataset(dataset_id)
    table = dataset.table(table_id)
    try:
        json_object = json.loads(rows)
        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        job_config.schema = format_schema(table_schem
        job = client.load_table_from_json(json_object, table, job_config = job_config)
        job.result()
    except GoogleAPICallError: # or TimeoutError or TypeError
      return {'message': 'Unable to save failed rows to Bigquery'}
    return { 'count': 42,
             'columns': ['id', 'amount']
             'message': f'Faled rows saved to {table_id}'}
```
Then, configure the failed row processor in a scan builder as per the example below.
```python
# scan_builder construction
scan_builder = ScanBuilder()
scan_builder.failed_row_processor = BigQueryRowProcessor()
```