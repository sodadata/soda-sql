# Send sample data to Soda Cloud

When creating new monitors in Soda Cloud, you may find it useful to review sample data from your dataset to help you determine the kinds of [tests](/docs/soda-sql/tests.md) to run when Soda SQL scans your data; see the image below. For this reason, you may wish to configure a `samples` [configuration key](/docs/soda-sql/scan-yaml.md#scan-yaml-table-configuration-keys) in Soda SQL.

![sample-data](/docs/assets/images/sample-data.png)


## Add a sample configuration key

DO NOT use sample data if your dataset contains sensitive information or personally identifiable information (PII). For security, you can [disable the sample data feature](#disable-sample-data), or [reroute failed sample data](#reroute-sample-data-for-a-dataset) to an alternate location.

1. If you have not already done so, [connect Soda SQL to your Soda Cloud account](/docs/soda-sql/connect_to_cloud.md).
2. Add a `samples` configuration key to your scan YAML file according to the Scan YAML example below; use `table_limit` to define a value that represents the numerical threshold of rows in a dataset that Soda SQL sends to Soda Cloud after it executes a test during a scan. It yields a sample of the data from your dataset in the **Sample Data** tab when you are creating a new monitor; see image above. A sample contains the first *n* number of rows from the dataset, according to the limit you specify.
3. Save the changes to your scan YAML file, then run a scan on that dataset.
```shell
soda scan warehouse.yml/tables/orders.yml
```
4. In your Soda Cloud account, navigate to the **Monitors** dashboard. Click the stacked-dots icon to **Create Monitor**. Note that in the first step of the guided monitor creation, you can review sample data from your dataset that Soda SQL collected during its last scan of your dataset. 

#### Scan YAML Example

```yaml
table_name: orders
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  ...
samples:
  table_limit: 50
tests:
  - row_count > 0
columns:
  orderid:
    valid_format: uuid
    tests:
      - invalid_percentage <= 3
```

Using the example scan YAML above, the scan executes both tests against all the data in the dataset, but it only sends a maximum of 50 rows of data and metadata to Soda Cloud for review as sample data when creating a new monitor for the `orders` dataset.

The snippet below displays the CLI output of the query that counts the rows in the dataset; Soda SQL counts 193 rows but only sends 50 as a sample to Soda Cloud.

```shell
  | ...
  | Executing SQL query:
SELECT *
FROM "public"."orders"
LIMIT 50;
  | SQL took 0:00:00.074957
  | Sent sample orders.sample (50/193) to Soda Cloud
  | ...
```

## Disable sample data

Where your datasets contain sensitive or private information, you may *not* want to send sample data from your data source to Soda Cloud. In such a circumstance, you can disable the feature completely in Soda Cloud.

To prevent Soda Cloud from receiving any sample data or failed row samples for any datasets in any data sources to which you have connected your Soda Cloud account, proceed as follows:

1. As an Admin, log in to your Soda Cloud account and navigate to **your avatar** > **Organization Settings**.
2. In the **Organization** tab, check the box to "Disable storage of sample data and failed row samples in Soda Cloud.", then **Save**. 

Alternatively, you can prevent Soda SQL from sending metadata or samples to Soda Cloud by using one of the following methods:
* To prevent Soda SQL from sending an individual dataset's scan results or samples to Soda Cloud, use the [`--offline` option](/docs/soda-sql/scan.md#add-scan-options) when you run a scan.
* To prevent Soda SQL from sending specific column scan results or samples, configure an [`excluded_columns` configuration key](/docs/soda-sql/scan-yaml.md#scan-yaml-table-configuration-keys) in your scan YAML file.

### Reroute sample data for a dataset

Use a `SampleProcessor` to send a dataset's samples to a secure location within your organization's infrastructure, such as an Amazon S3 bucket or Google Big Query. Note that you can only configure sample data rerouting for individual datasets, and only for those scans that you have scheduled programmatically. In Soda Cloud, users looking for sample data see the message you define advising them where they can access and review sample data for the dataset.

#### Reroute to Amazon S3

First, configure a `SampleProcessor` according to the following example.

```python
import boto
import json

from soda.scan.SampleProcessor

class S3SampleProcessor(SampleProcessor):
  # Override the process function
  def process(context) → dict:
    file_name = 'sample_rows.json'
    with open(file_name, 'w', encoding='uft-8') as f:
      json.dump(, f)

    s3_client = boto3.client('s3')
    if object_name is None:
      object_name = os.path.basename(file_name)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return {'message': 'Unable to load sample data into S3'}
    return {'message':
             f'Sample data is stored in S3://{bucket_name}/{file_name}'}
```
Then, configure the sample processor in a scan builder as per the example below.
```python
# scan_builder construction
scan_builder.sample_processor = S3SampleProcessor()
scan_result = scan_builder.build().execute()
```
<br />

#### Reroute to Google Big Query using existing credentials

This configuration uses the Big Query access credentials that Soda SQL uses. These credentials must have the appropriate service account and scopes in Big Query which give Soda SQL write permission on the table.

First, configure a `SampleProcessor` according to the following example. Note that the `client` parameter points to different objects for different warehouses.
```python
import bigquery
from soda.scan.SampleProcessor

class BigQuerySampleProcessor(SampleProcessor):
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
                 'message': f'Sample data is stored in {table_id}'}
    else:
       return {'message': 'Unable to save sample data to Bigquery'}
```
Then, configure the sample processor in a scan builder as per the example below.
```python
# scan_builder construction
scan_builder.sample_processor = BigQuerySampleProcessor()
scan_result = scan_builder.build().execute()
```
<br />

#### Reroute to Google Big Query using separate credentials

This configuration *does not* use the Big Query access credentials that Soda SQL uses. The separate credentials must have the appropriate service account and scopes in Big Query which give Soda SQL write permission on the table.

First, configure a `SampleProcessor` according to the following example. Note that the `client` parameter points to different objects for different warehouses.
```python
import json
import bigquery
from soda.scan.SampleProcessor

class BigQuerySampleProcessor(SampleProcessor):
  # Override process function
  # context: sql, connection, sample_reference
  def process(context) → dict:

    table_schema = {
     ## Define Schema for the sample dataset.table
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
      return {'message': 'Unable to save sample data to Bigquery'}
    return { 'count': 42,
             'columns': ['id', 'amount']
             'message': f'Sample data is stored in {table_id}'}
```
Then, configure the samples processor in a scan builder as per the example below.
```python
# scan_builder construction
scan_builder = ScanBuilder()
scan_builder.sample_processor = BigQuerySampleProcessor()
```