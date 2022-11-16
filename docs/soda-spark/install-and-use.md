# Install and use Soda Spark

Soda Spark is an extension of 
[Soda SQL](/docs/soda-sql/quick-start-soda-sql.md) that allows you to run Soda
SQL functionality programmatically on a 
<a href="https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.DataFrame.html" target="_blank">Spark DataFrame</a>. Reference the Soda SQL documentation to learn how to use Soda Spark, particularly how to [define tests](/docs/soda-sql/tests.md) in a [scan YAML file](/docs/soda-sql/scan-yaml.md). 

[Requirements](#requirements)
[Compatibility](#compatibility)
[Install Soda Spark](#install-soda-spark)
[Install Soda Spark on Windows](#install-soda-spark-on-windows)
[Use Soda Spark](#use-soda-spark)
[How Soda Spark works](#how-soda-spark-works)
<br />

## Requirements

To install Soda Spark on a cluster, such as a Kubernetes cluster or a Databricks cluster, install <a href="https://packages.debian.org/buster/libsasl2-dev" target="_blank"> `libsasl2-dev` </a> *before* installing Soda Spark. For Ubuntu users, install `libsasl2-dev` using the following command: 
```shell
sh sudo apt-get -y install unixodbc-dev libsasl2-dev gcc python-dev
```

To use Soda Spark, you must have installed the following on your system.

* **Python 3.7** or greater. To check your existing version, use the CLI command: `python --version`
* **Pip 21.0** or greater. To check your existing version, use the CLI command: `pip --version`

For Linux users only, install the following:

* On Debian Buster: `apt-get install g++ unixodbc-dev python3-dev libssl-dev libffi-dev`
* On CentOS 8: `yum install gcc-c++ unixODBC-devel python38-devel libffi-devel openssl-devel`


## Install Soda Spark

1. (Optional) Best practice dictates that you install the Soda Spark package using a virtual environment. In your command-line interface tool, create a virtual environment in the `.venv` directory using the commands below. Depending on your version of Python, you may need to replace `python` with `python3` in the first command.
```shell
python -m venv .venv
source .venv/bin/activate
```
2. Upgrade pip.
```shell
pip install --upgrade pip
```
3. Execute the following command to install the Soda Spark package.

``` sh
pip install soda-spark
```

<br />

#### Troubleshoot


**Problem:** I tried installing `soda-spark` on a Databricks cluster and the `pip install` fails. Both Python and pip meet the install requirements. <br />
**Solution:** Install `libsasl2-dev`, then use `pip install soda-spark`.
<br />

**Problem:** As an Ubuntu user, I tried installing `soda-spark` on a Databricks cluster and the `pip install` fails with a `Py4JJavaError`.  <br />
**Solution:** Install `libsasl2-dev` by executing `%sh sudo apt-get -y install unixodbc-dev libsasl2-dev gcc python-dev` first, then use `pip install soda-spark`.
<br />

## Install Soda Spark on Windows

1. From the command-line, check existing distributions by running the following command.
```shell
wsl --list --online
```
2. Install the Ubuntu distribution using the following command. It opens in a new tab.
```shell
wsl --install -d Ubuntu
```
3. When the installation completes, reboot your system, then set a username and password at the prompt.
4. Validate that the package is up-to-date. 
```shell
sudo apt update
```
5. Install the following packages.
```shell
sudo apt-get -y install unixodbc-dev libsasl2-dev gcc python-dev
```
6. Install Python and pip.
```shell
sudo apt install python3 python3-pip
```
7. Confirm that the version of Python you installed is version 3.7 or greater.
```shell
python3 --version
```
8. Confirm that the version of pip you installed is 21.0 or greater.
```shell
pip -- version
```
9. Install Virtualenv, a tool that enables you to create an isolated Python environment. Replace the value of `3.8` with the value of your own Python version.
```shell
sudo apt install python3.8-venv
```
10. Create, then activate, a virtual environment.
```shell
python3 -m venv sodaspark
source sodaspark/bin/activate
```
11. Upgrate pip in the virtual environment.
```shell
pip install --upgrade pip
```
12. Install the Soda Spark package in the virtual environment.
```shell
pip install soda-spark
```
13. Install the findspark package in the virtual environment.
```shell
pip install findspark
```
14. Install the Java Runtime Environment for Windows in the virtual environment.
```shell
sudo apt install openjdk-11-jre-headless
```
 

## Use Soda Spark
As an extension of Soda SQL, Soda Spark allows you to run Soda
SQL functionality programmatically on a Spark DataFrame. Reference the Soda SQL documentation to learn how to use Soda Spark. 

From your Python prompt, execute the following commands to programmatically run Soda SQL functionality.

``` python
>>> from pyspark.sql import DataFrame, SparkSession
>>> from sodaspark import scan
>>>
>>> spark_session = SparkSession.builder.getOrCreate()
>>>
>>> id = "a76824f0-50c0-11eb-8be8-88e9fe6293fd"
>>> df = spark_session.createDataFrame([
...	   {"id": id, "name": "Paula Landry", "size": 3006},
...	   {"id": id, "name": "Kevin Crawford", "size": 7243}
... ])
>>>
>>> scan_definition = ("""
... table_name: demodata
... metrics:
... - row_count
... - max
... - min_length
... tests:
... - row_count > 0
... columns:
...   id:
...     valid_format: uuid
...     tests:
...     - invalid_percentage == 0
... """)
>>> scan_result = scan.execute(scan_definition, df)
>>>
>>> scan_result.measurements
[Measurement(metric='schema', ...), Measurement(metric='row_count', ...), ...]
>>> scan_result.test_results
[TestResult(test=Test(..., expression='row_count > 0', ...), passed=True, skipped=False, ...)]
>>>
```

Alternatively, you can prepare a [scan YAML file](/docs/soda-sql/scan-yaml.md) that Soda Spark uses to prepare SQL queries to run against your data.

``` python
>>> scan_yml = "static/demodata.yml"
>>> scan_result = scan.execute(scan_yml, df)
>>>
>>> scan_result.measurements
[Measurement(metric='schema', ...), Measurement(metric='row_count', ...), ...]
>>>
```

## Send scan results to Soda Cloud

Use the following command to send Soda Spark scan results to Soda cloud. Use [Soda Cloud documentation](/docs/soda-sql/connect_to_cloud.md) to learn how to generate API keys to connect Soda Spark to Soda Cloud.

``` python
>>> import os
>>> from sodasql.soda_server_client.soda_server_client import SodaServerClient
>>>
>>> soda_server_client = SodaServerClient(
...     host="cloud.soda.io",
...     api_key_id=os.getenv("API_PUBLIC"),
...     api_key_secret=os.getenv("API_PRIVATE"),
... )
>>> scan_result = scan.execute(scan_yml, df, soda_server_client=soda_server_client)
>>>
```

## How Soda Spark works

When you execute Soda Spark, it completes the following tasks:

1. It sets up the scan using the Spark dialect and a <a href="https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.SparkSession.html" target="_blank">Spark session</a> as a [warehouse](/docs/soda-sql/warehouse.md) connection.
2. It creates, or replaces, a 
	<a href="https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.DataFrame.createOrReplaceGlobalTempView.html" target="_blank">global temporary view</a>
   for the Spark DataFrame.
3. It executes the Soda scan on the temporary view.
