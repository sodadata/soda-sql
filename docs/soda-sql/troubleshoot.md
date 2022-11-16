# Troubleshoot Soda SQL


## Install and upgrade Soda SQL

**Problem:** There are known issues on Soda SQL when using pip version 19. <br />
**Solution:** Upgrade `pip` to version 20 or greater using the following command:
```shell
$ pip install --upgrade pip
```
<br />

**Problem:** Upgrading Soda SQL does not seem to work. <br />
**Solution:** Run the following command to skip your local cache when upgrading your Soda SQL version:
```shell
$ pip install --upgrade --no-cache-dir soda-sql-yourdatasource
```
<br />

**Problem:** I can't run the `soda` command in my CLI. It returns `command not found: soda`. <br />
**Solution:** If you followed the instructions to [install Soda SQL](/docs/soda-sql/installation.md) and still received the error, you may need to adjust your `$PATH` variable. 
1. Run the following command to find the path to your installation of Python, replacing `soda-sql-postgresql` with the install package that matches the type of warehouse you use if not PostgreSQL:<br />
`pip show soda-sql-postgresql`
<br /> <br /> The output indicates the Location that looks something like this example:
```shell
...
Location: /Users/yourname/Library/Python/3.8/lib/python/site-packages
...
```
2. Add the location to your `$PATH` variable using the `export PATH` command as follows:
`'export PATH=$PATH:/Users/yourname/Library/Python/3.8/bin soda'` <br />
3. Run the `soda` command again to receive the following output:<br />
```shell
Usage: soda [OPTIONS] COMMAND [ARGS]...
  Soda CLI version 2.1.xxx
Options:
  --help  Show this message and exit.
Commands:
  analyze  Analyze tables and scaffold SCAN YAML
  create   Create a template warehouse.yml file
  ingest   Ingest test information from different tools
  scan     Compute metrics and run tests for a given table
```

<br />

**Problem:** When you run `soda analyze` you get an an authentication error. <br />
**Solution:** Check to see if you have another instance of Postgres already running on port 5432. If so, try stopping or uninstalling the Postgres instance, then run `soda analyze` again. 
<br />

## Scans and tests with Soda SQL

**Problem:** Soda SQL scans produce errors in the CLI. <br />
**Solution:** Check your `warehouse.yml`, `env_vars.yml`, and scan YAML files for proper spacing, indentation, and verbiage. See [Warehouse YAML](/docs/soda-sql/warehouse.md) and [Scan YAML](/docs/soda-sql/scan-yaml.md).
<br />

**Problem:** When I run a scan, I get this error.
```shell
UnicodeEncodeError: 'latin-1' codec can't encode character '\u20ac' in position 431: ordinal not in range(256)
```
**Solution:** Soda SQL does not support scans of tables using Latin-1 encoding. Adjust the tables to UTF-8 encoding to run a scan.
<br />

**Problem:** When using an historic metric, you get an scan error message that advises you that there are insufficient measurements to complete the scan.

**Solution:** The Cloud Metric Store does not contain enough historic measurements to execute the test you have defined. For example, if you defined a test to count back to the seventh historic measurement but your Cloud Metric Store only contains three historic measurements, Soda SQL cannot complete the scan. Consider lowering the count-back number in your test, then run the scan again.
<br />

## Data source connections with Soda SQL

**Problem:** I get errors in the CLI when I run `soda analyze` on my MS SQL server data source.   <br />
**Solution:** Connecting Soda SQL to MS SQL servers is still in experimental phase. You may encounter errors before this data source connection type is stabilized.
<br />

**Problem:**  I use Amazon Athena and I'm having trouble connecting Soda SQL to data in an S3 bucket. <br />
**Solution:** If you have [followed the instructions](/docs/soda-sql/configure.md#configuration-instructions) to configure your warehouse YAML and have added your AWS access key ID and secret access key to your env_vars YAML file but are still not connecting, you may need to adjust the S3 bucket setup and user profile permissions. 

When you connect Soda SQL to Athena to run scans on data in an S3 bucket, Soda SQL uses PyAthena (the Python DB API client for Amazon Athena) to output its scan results to the staging directory in the same S3 bucket. As such, the user profile that Soda SQL uses to connect to Athena (the Athena access keys you configured in your env_vars YAML files) must have write permission to the staging directory. If the user profile doesn't have the correct write permissions, the issue manifests in Soda SQL as a connection error. Instead, as best practice, separate the buckets.

1. Create a new Athena account and restrict the user profile with a policy that specifies that it can only write to the S3 bucket with the staging directory.
2. Create a new S3 bucket for your staging directory, then configure a separate warehouse YAML to access the staging directory. For example: 
```yaml
name: athena-query-results
connection:
    type: athena
    catalog: AwsDataCatalog
    database: test
    access_key_id: env_var(AWS_ACCESS_KEY_ID)
    secret_access_key: env_var(AWS_SECRET_ACCESS_KEY)
    role_arn: 
    region: eu-west-1
    staging_dir: <YOUR STAGING PATH IN AWS S3>
...
```

However, if you do not want to create a new S3 bucket for the staging directory, you can adjust the existing settings for the user profile you use to connect Soda SQL to Athena to include the following actions:
* `GetBucketLocation`
* `ListAllMyBuckets`
* `ListBucket`
* `GetObject`
* `ListBucketMultipartUploads`
* `ListMultipartUploadParts`
* `AbortMultipartUpload`
* `PutObject`
 
<br />

## Soda Cloud

**Problem:** You open the monitor whose test failed during a scan but cannot click the **Failed Rows** tab. <br />
**Solution:** Click a failed data point in the chart that shows the monitor's scan results over time. This action identifies the specific set of failed rows associated with an individual scan result so it can display the failed rows associated with that individual scan. 
<br />
