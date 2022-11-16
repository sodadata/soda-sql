# Quick start for Soda SQL and Soda Cloud 


![soda-sql-logo](/docs/assets/images/soda-sql-logo.png)
Use your command-line interface to connect Soda SQL to a demo warehouse, create and examine the tests that surface “bad” data in a table, then run your first scan in a few minutes. <br />
<br />

![soda-cloud-logo](/docs/assets/images/soda-cloud-logo.png)
After you run your scan from the command-line, consider going further by signing up for a free trial account in Soda Cloud, the web application that offers data quality visualizations and much more. 

[Tutorial prerequisites](#tutorial-prerequisites) 
[Create a demo warehouse](#create-a-demo-warehouse)
[Connect Soda SQL to the warehouse](#connect-soda-sql-to-the-warehouse)
[Create and examine tests](#create-and-examine-tests)
[Run a scan](#run-a-scan) 
[Connect Soda SQL to Soda Cloud (Optional)](#connect-soda-sql-to-soda-cloud) 
<br />



## Tutorial prerequisites
* a GitHub account
* a recent version of <a href="https://docs.docker.com/get-docker/" target="_blank">Docker</a>
* <a href="https://docs.docker.com/compose/install/" target="_blank">Docker Compose</a> that is able to run docker-compose files version 3.9 and later
* a code editor such as Sublime or Visual Studio Code

## Create a demo warehouse

In the context of Soda SQL, a warehouse is a type of data source that represents a SQL engine or database such as Snowflake, Amazon Redshift, or PostgreSQL. 

For this tutorial, use Docker to build a demo PostgreSQL warehouse from a <a href="https://github.com/sodadata/tutorial-demo-project" target="_blank">Soda tutorial-demo-project</a> repository in GitHub. The warehouse contains public <a href="https://data.cityofnewyork.us/Transportation/Bus-Breakdown-and-Delays/ez4e-fazm" target="_blank">NYC School Bus Breakdowns and Delays</a> data that you can use to see the Soda SQL CLI tool in action. All the instructions in this tutorial reference this demo warehouse.

Use the instructions below to set up the demo warehouse using a script, or set it up manually by cloning the repo. When you clone the repo and spin up the Docker instance, you can use a code editor to edit YAML files later in the tutorial. 

### Set up with a script

From the command-line, run the following script:
```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/sodadata/tutorial-demo-project/main/scripts/setup.sh)"
```

#### Troubleshoot
**Problem:** When running the script on a Mac, you get an error such as `failed to solve with frontend dockerfile.v0: failed to read dockerfile: error from sender: open /Users/<user>/.Trash: operation not permitted.`

**Solution:** You need to grant Full Disk Access to the Terminal application. Go to System Preferences > Security & Privacy > Privacy, then select Full Disk Access. Check the box next to Terminal to grant full disk access.

### Set up manually

1. Clone the <a href="https://github.com/sodadata/tutorial-demo-project" target="_blank">tutorial-demo-project</a> GitHub repo to your local environment.
2. In the command-line, navigate to the tutorial repo's directory. 
```shell
cd tutorial-demo-project
```
3. If you have not already done so, start Docker. Then, build the Docker containers (the `-d` flag means "detached" which means that you do not need to keep the terminal running for the docker containers to continue to run.). 
```shell
docker-compose up -d
``` 
4. (Optional) Validate that the setup is complete. 
```shell
docker ps -a | grep soda
```  
Output:
```
CONTAINER ID   IMAGE                                    COMMAND                  CREATED       STATUS         PORTS                                       NAMES
90b555b29ccd   tutorial-demo-project_soda_sql_project   "/bin/bash"              3 hours ago   Exited (2) 3 seconds ago   0.0.0.0:8001->5432/tcp, :::8001->5432/tcp   tutorial-demo-project_soda_sql_project_1
d7950300de7a   postgres                                 "docker-entrypoint.s…"   3 hours ago   Up 3 seconds   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   tutorial-demo-project_soda_sql_tutorial_db_1
```
5. To run Soda commands, you need to get into the container's shell. From the project's root directory where the `docker-compose.yml` file exists, run the following command:

```bash
docker-compose run --rm soda_sql_project "cd /workspace && /bin/bash"
```
This command puts you into the container's shell with a prompt like the following:

```bash
root@90461262c35e:/workspace# 
```


## Connect Soda SQL to the warehouse

Though this tutorial uses PostgreSQL, there are many [install packages for Soda SQL](/docs/soda-sql/installation.md#install) that correspond to different warehouse types.   

1. From your command-line interface, verify the installation of Soda SQL in the demo environment using the `soda` command. The CLI output appears as per the following. 
```shell
Usage: soda [OPTIONS] COMMAND [ARGS]...
  Soda CLI version 2.x.x
Options:
  --help  Show this message and exit.
Commands:
  analyze  Analyze tables and scaffold SCAN YAML
  create   Create a template warehouse.yml file
  ingest   Ingest test information from different tools
  scan     Compute metrics and run tests for a given table
```
2. Create, then navigate to a new Soda SQL warehouse directory. The example below creates a directory named `new_york_bus_breakdowns`.
```shell
mkdir new_york_bus_breakdowns
cd new_york_bus_breakdowns
```
3. Use the `soda create postgres` command to create and pre-populate two files that enable you to configure connection details for Soda SQL to access your warehouse:
* a `warehouse.yml` file which stores access details for your warehouse ([read more](/docs/soda-sql/warehouse.md))
* an `env_vars.yml` file which securely stores warehouse login credentials ([read more](/docs/soda-sql/warehouse.md#env_vars-yaml-file))<br />

Command:
```shell
soda create postgres
```
Output:
```shell
  | Soda CLI version 2.x.x
  | Creating warehouse YAML file warehouse.yml ...
  | Adding env vars for postgres to /root/.soda/env_vars.yml
  | Review warehouse.yml by running command
  |   cat warehouse.yml
  | Review section postgres in ~/.soda/env_vars.yml by running command
  |   cat ~/.soda/env_vars.yml
  | Then run the soda analyze command
  | Starting new HTTPS connection (1): collect.soda.io:443
  | https://collect.soda.io:443 "POST /v1/traces HTTP/1.1" 200 0
```
4. Optionally, use the following commands to review the contents of the two YAML files Soda SQL created. Soda SQL automatically lists the fields for which it requires values, and pre-populates some of the values. 

Command:
```shell
cat warehouse.yml
```
Output:
```shell
name: postgres
connection:
  type: postgres
  host: localhost
  port: '5432'
  username: env_var(POSTGRES_USERNAME)
  password: env_var(POSTGRES_PASSWORD)
  database: your_database
  schema: public
```
Command:
```shell
cat ~/.soda/env_vars.yml
```
Output:
```shell
postgres:
  POSTGRES_USERNAME: Eg johndoe
  POSTGRES_PASSWORD: Eg abc123
```
5. Because this tutorial uses a sample warehouse, you can use the demo `warehouse.yml` and `env_vars.yml` files that connect to our sample NYC School Bus Breakdowns and Delays data. Use the following commands to navigate to the demo directory before proceeding.
```shell
cd ..
cd new_york_bus_breakdowns_demo
```
<br />

If you were connecting to your own warehouse, you would [follow the detailed instructions](/docs/soda-sql/configure.md) to edit the `warehouse.yml` and `env_vars.yml` file and provide values specific to your warehouse so that Soda SQL could access it. 

## Create and examine tests

1. From the `new_york_bus_breakdowns_demo` directory, use the `soda analyze` command to get Soda SQL to sift through the contents of the demo warehouse and automatically prepare a scan YAML file for each table it discovers. Soda SQL puts the YAML files in a new `/tables` directory in the `new_york_bus_breakdowns_demo` project directory. Read more about [scan YAML](/docs/soda-sql/scan-yaml.md) files.<br />

Command:
```shell
soda analyze
```
Output:
```
  | 2.x.xxx
  | Analyzing warehouse.yml ...
  | Querying warehouse for tables
  | Creating tables directory tables
  | Executing SQL query: 
SELECT table_name 
FROM information_schema.tables 
WHERE lower(table_schema)='new_york'
  | SQL took 0:00:00.068775
...
  | SQL took 0:00:00.030745
  | Creating tables/breakdowns.yml ...
  | Next run 'soda scan warehouse.yml tables/breakdowns.yml' to calculate measurements and run tests
  | Starting new HTTPS connection (1): collect.soda.io:443
  | https://collect.soda.io:443 "POST /v1/traces HTTP/1.1" 200 0
```
2. Use the following command to review the contents of the new scan YAML file that Soda SQL created and named `breakdowns.yml`. `breakdowns` is the only table in the warehouse. <br />

Command:
```shell
cat tables/breakdowns.yml
```
<br />
Output:
```yaml
table_name: breakdowns
metrics:
  - row_count
  - missing_count
  - missing_percentage
  - values_count
  - values_percentage
  - invalid_count
  - invalid_percentage
  - valid_count
  - valid_percentage
  - avg_length
  - max_length
  - min_length
  - avg
  - sum
  - max
  - min
  - stddev
  - variance
tests:
  - row_count > 0
columns:
  school_year:
    valid_format: date_inverse
    tests:
      - invalid_percentage == 0
  bus_no:
    valid_format: number_whole
    tests:
      - invalid_percentage <= 20
  schools_serviced:
    valid_format: number_whole
    tests:
      - invalid_percentage <= 15
```

When it created this file, Soda SQL pre-populated it with four tests it deemed useful based on the data in the table it analyzed. Read more about [Defining tests](/docs/soda-sql/tests.md) and the [Anatomy of the scan YAML file](/docs/soda-sql/scan-yaml.md#anatomy-of-the-scan-yaml-file).

| Test | Applies to | Description |
| ---- | ---------- | ----------- |
| `row_count > 0` | the entire table | Tests that the table contains rows, that it is not empty. |
| `invalid_percentage == 0` | `school_year` column in the table | Tests that all values in the column adhere to the `date_inverse` format. Read more about [valid format values](/docs/soda-sql/sql_metrics.md#valid-format-values). |
| `invalid_percentage <= 20` | `bus_no` column in the table | Tests that at least 80% of the values in the column are whole numbers. |
| `invalid_percentage <= 15` | `schools_serviced` column in the table | Tests that at least 85% of the values in the column are whole numbers. |


## Run a scan

1. Use the `soda scan` command to run tests against the data in the breakdowns table. As input, the command requires:
* the name of the warehouse to scan
* the filepath and name of the scan YAML file <br />

Command:
```shell
soda scan warehouse.yml tables/breakdowns.yml
```
2. Examine the output of the command, in particular the **Scan summary** at the bottom that indicates the results of the tests Soda SQL ran against your data. In this example, all the tests passed which indicates that there are no issues with the data.<br />

Output:
```shell
  | 2.x.xx
  | Scanning tables/breakdowns.yml ...
  | ...
  | No Soda Cloud account configured
  | Executing SQL query: 
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE lower(table_name) = 'breakdowns' 
  AND table_catalog = 'sodasql_tutorial' 
  AND table_schema = 'new_york'
  | SQL took 0:00:00.062634
  ...
  | Test test(row_count > 0) passed with measurements {"expression_result": 199998, "row_count": 199998}
  | Test column(school_year) test(invalid_percentage == 0) passed with measurements {"expression_result": 0.0, "invalid_percentage": 0.0}
  | Test column(bus_no) test(invalid_percentage <= 20) passed with measurements {"expression_result": 19.99919999199992, "invalid_percentage": 19.99919999199992}
  | Test column(schools_serviced) test(invalid_percentage <= 15) passed with measurements {"expression_result": 12.095620956209562, "invalid_percentage": 12.095620956209562}
  | Executed 2 queries in 0:00:03.291901
  | Scan summary ------
  | 239 measurements computed
  | 4 tests executed
  | All is good. No tests failed.
  | Exiting with code 0
  | Starting new HTTPS connection (1): collect.soda.io:443
  | https://collect.soda.io:443 "POST /v1/traces HTTP/1.1" 200 0
```
3. (Optional) Open the `tables/breakdowns.yml` file locally in a code editor, adjust the test for the `school_year` column to `invalid_percentage == 5`, then save the change to the file.
4. (Optional) Run the same scan again to see the output of a failed test.<br />

Command:
```shell
soda scan warehouse.yml tables/breakdowns.yml
```
Output:
```shell
...
  | Test test(row_count > 0) passed with measurements {"expression_result": 199998, "row_count": 199998}
  | Test column(school_year) test(invalid_percentage == 5) failed with measurements {"expression_result": 0.0, "invalid_percentage": 0.0}
  | Test column(bus_no) test(invalid_percentage <= 20) passed with measurements {"expression_result": 19.99919999199992, "invalid_percentage": 19.99919999199992}
  | Test column(schools_serviced) test(invalid_percentage <= 15) passed with measurements {"expression_result": 12.095620956209562, "invalid_percentage": 12.095620956209562}
  | Executed 2 queries in 0:00:02.454419
  | Scan summary ------
  | 239 measurements computed
  | 4 tests executed
  | 1 of 4 tests failed:
  |   Test column(school_year) test(invalid_percentage == 5) failed with measurements {"expression_result": 0.0, "invalid_percentage": 0.0}
  | Exiting with code 1
  | Starting new HTTPS connection (1): collect.soda.io:443
  | https://collect.soda.io:443 "POST /v1/traces HTTP/1.1" 200 0
```
5. (Optional) If you like, adjust or add more tests to the `breakdowns.yml` file to further explore the things that Soda SQL can do. Use a code editor to edit YAML files.

To exit the workspace in your command-line interface, type `exit` then press enter.<br />
OR <br />
Continue to the next section to connect Soda SQL to a Soda Cloud account.

## Connect Soda SQL to Soda Cloud 

Though you can use Soda SQL as a standalone CLI tool to monitor data quality, you may wish to connect to the Soda Cloud web application that vastly enriches the data quality monitoring experience. 

Beyond increasing the observability of your data, Soda Cloud enables you to automatically detect anomalies, and view samples of the rows that failed a test during a scan. Integrate Soda Cloud with your Slack workspace to collaborate with your team on data monitoring.

Soda SQL uses an API to connect to Soda Cloud. To use the API, you must generate API keys in your Soda Cloud account, then add them to the warehouse YAML file that Soda SQL created. When it runs a scan, Soda SQL pushes the test results to Soda Cloud. 


1. If you have not already done so, create a Soda Cloud account at <a href="https://cloud.soda.io/signup" target="_blank"> cloud.soda.io</a>.
2. Open the `warehouse.yml` file in a code editor, then add the following to the file:
```yaml
soda_account:
  host: cloud.soda.io
  api_key_id: env_var(API_PUBLIC)
  api_key_secret: env_var(API_PRIVATE)
```
3. Save the `warehouse.yml` file.
4. In the `tutorial-demo-project` repo, open the `data/env_vars.yml` file in a code editor, then add `API_PUBLIC` and `API_PRIVATE` as per the following. Note that `sodasql` corresponds to the `name` of the data source connection in `workspace/new_york_bus_breakdowns_demo/warehouse.yml`.
```yaml
sodasql:
  API_PUBLIC: 
  API_PRIVATE: 
```
5. In Soda Cloud, navigate to **your avatar** > **Profile** > **API Keys**, then click the plus icon to generate new API keys.
    * Copy the **API Key ID**, then paste it into the `env_vars.yml` file as the value for `API_PUBLIC`.
    * Copy the **API Key Secret**, then paste it into the `env_vars.yml` file as the value for `API_PRIVATE`.
6. Save the changes to the `env_vars.yml` file. Close the **Create API Key** dialog box in your Soda Cloud account.
7. From the command-line, in the `new_york_bus_breakdowns_demo` directory, use Soda SQL to scan the table again.
```shell
$ soda scan warehouse.yml tables/breakdowns.yml
```
8. Go to your Soda Cloud account in your browser and navigate to the **Monitors** dashboard. Review the results of your scan in **Monitor Results**. 
![cloud-tutorial-results](/docs/assets/images/cloud-tutorial-results.png)
9. Navigate to the **Datasets** dashboard, then click to select the **breakdowns** table to review statistics and metadata about the table.
![dataset-metadata](/docs/assets/images/dataset-metadata.png)
10. Explore Soda Cloud!
* integrate your Slack workspace to receive notifications of failed tests and collaborate on data quality investigations
* set up alerts and notifications for the monitors in your account
* open and track data quality incidents and collaborate to resolve them with your team in Slack

To exit the workspace in your command-line interface, type `exit` then press enter.