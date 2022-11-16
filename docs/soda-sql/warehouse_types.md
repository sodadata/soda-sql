# Data source configurations for Soda SQL

Soda SQL needs connection details in order to access your data source to scan your data. Each type of data source uses different configuration parameters. To set the data source configurations in your [warehouse YAML](/docs/soda-sql/warehouse.md), use the following example configurations that correspond to each kind of data source that Soda SQL supports.

You can connect Soda Core to your Soda Cloud account. To communicate with your data source, Soda Cloud uses a Network Address Translation (NAT) gateway with the IP address 54.78.91.111. You may wish to add this IP address to your data source's passlist.

[Amazon Athena](#amazon-athena) 
[Amazon Redshift](#amazon-redshift) 
[Apache Hive (Experimental)](#apache-hive-experimental) 
[Apache Spark](#apache-spark) 
[Google Cloud Platform Big Query](#gcp-big-query) 
[Microsoft SQL Server (Experimental)](#microsoft-sql-server-experimental) 
[MySQL (Experimental)](#mysql-experimental) 
[PostgreSQL](#postgresql) 
[Snowflake](#snowflake) 
[Trino (Experimental)](#trino-experimental) 
[Troubleshoot data source connections](/docs/soda-sql/troubleshoot.md#data-source-connections)<br />


## Amazon Athena

```yaml
name: my_athena_project
connection:
    type: athena
    catalog: AwsDataCatalog
    database: sodalite_test
    access_key_id: env_var(AWS_ACCESS_KEY_ID)
    secret_access_key: env_var(AWS_SECRET_ACCESS_KEY)
    role_arn: 
    region: eu-west-1
    staging_dir: <YOUR STAGING PATH IN AWS S3>
...
```

| Property  | Required | Notes |
| --------  | -------- |-------- |
| type | required |  |
| catalog |optional | Default is `AwsDataCatalog`. |
| database | required |  |
| staging_dir |  required |  |
| access_key_id |  optional | Use environment variables to retrieve this value securely. |
| secret_access_key | optional | Use environment variables to retrieve this value securely. |
| role_arn |optional | The [Amazon Resource Name](https://docs.aws.amazon.com/credref/latest/refdocs/setting-global-role_arn.html) of an IAM role that you want to use. | 
| region |  optional |  |

Access keys and IAM role are mutually exclusive: if you provide values for `access_key_id` and `secret_access_key`, you cannot use Identity and Access Management role; if you provide value for `role_arn`, then you cannot use the access keys. Refer to [Identity and Access Management in Athena](https://docs.aws.amazon.com/athena/latest/ug/security-iam-athena.html) for details.

Refer to [Troubleshoot warehouse connections](/docs/soda-sql/troubleshoot.md#warehouse-connections) for help with Athena connection issues.

## Amazon Redshift

```yaml
name: my_redshift_project
connection:
    type: redshift
    host: <YOUR AMAZON REDSHIFT HOSTNAME>
    username: soda
    password: <YOUR AMAZON REDSHIFT PASSWORD>
    database: soda_agent_test
    schema: public
    access_key_id: env_var(AWS_ACCESS_KEY_ID)
    secret_access_key: env_var(AWS_SECRET_ACCESS_KEY)
    role_arn: 
    region: eu-west-1
...
```

| Property |  Required | Notes |
| -------- |  -------- | ----- |
| type    | required |  |
| host |  required |   |
| username  |  required |  |
| password  |  required |  |
| database  | required |  |
| schema    |  |  |
| access_key_id  | optional | Use environment variables to retrieve this value securely. |
| secret_access_key  | optional | Use environment variables to retrieve this value securely. |
| role_arn| optional | The [Amazon Resource Name](https://docs.aws.amazon.com/credref/latest/refdocs/setting-global-role_arn.html) of an IAM role that you want to use. |
| region | optional |  |

Access keys and IAM role are mutually exclusive: if you provide values for `access_key_id` and `secret_access_key`, you cannot use Identity and Access Management role; if you provide value for `role_arn`, then you cannot use the access keys. Refer to [Amazon Redshift Authorization parameters](https://docs.aws.amazon.com/redshift/latest/dg/copy-parameters-authorization.html) for details.

## Apache Hive (Experimental)

```yaml
name: my_hive_project
connection:
    type: hive
    host: localhost
    port: 10000
    username: env_var(HIVE_USERNAME)
    password: env_var(HIVE_PASSWORD)
    database: default
    authentication: None
    configuration:
      hive.execution.engine: mr
      mapreduce.job.reduces: 2
...
```

| Property |  Required | Notes |
| -------- |  -------- | ----- |
| type  | required  |  |
| host  | required  |  |
| port  | optional  |  |
| username  | required  | Use environment variables to retrieve this value securely. |
| password  | optional  | Use environment variables to retrieve this value securely. <br /> Use with `authentication='LDAP'` or `authentication='CUSTOM'` only <br /> |
| database | optional | |
| authentication | optional | The value of hive.server2.authentication used by HiveServer2 |
| hive.execution.engine | required | Input options are: <br /> `mr` (Map reduce, default) <br /> `tez` (Tez execution for Hadoop 2) <br /> `spark` (Spark execution for Hive 1.1.0 or later)|
| mapreduce.job.reduces | required | Sets the number of reduce tasks per job. Input `-1` for Hive to automatically determine the number of reducers. |


## Apache Spark

```yaml
name: my_spark_project
connection:
    type: spark
    host: localhost
    port: 10000
    username: env_var(SPARK_USERNAME)
    password: env_var(SPARK_PASSWORD)
    database: default
    authentication: None
    token: env_var(SPARK_TOKEN)
```

| Property |  Required | Notes |
| -------- |  -------- | ----- |
| type  | required  |  |
| host  | required  |  |
| port  | optional  |  |
| username  | optional  | Use environment variables to retrieve this value securely. |
| password  | optional  | Use environment variables to retrieve this value securely. <br /> Use with `authentication='LDAP'` or `authentication='CUSTOM'` only <br /> |
| database | optional | |
| authentication | optional | The value of hive.server2.authentication used by HiveServer2 |
| token | optional | 


## GCP Big Query

A note about BigQuery datasets: Google uses the term dataset slightly differently than Soda (and many others) do. 
* In the context of Soda, a dataset is a representation of a tabular data structure with rows and columns. A dataset can take the form of a table in PostgreSQL or Snowflake, a stream in Kafka, or a DataFrame in a Spark application. 
* In the context of BigQuery, a <a href="https://cloud.google.com/bigquery/docs/datasets-intro" target="_blank"> dataset</a> is "a top-level container that is used to organize and control access to your tables and views. A table or view must belong to a dataset..."

Instances of "dataset" in Soda documentation always reference the former.

Use the values Google Cloud Platform provides when you [create a service account](https://cloud.google.com/iam/docs/creating-managing-service-account-keys). Copy and paste the contents of your Big Query service account JSON key file into your `warehouse.yml` file. 

```yaml
name: my_bigquery_project
connection:
    type: bigquery
    account_info_json: '{
        "type": "service_account",
        "project_id": "...",
        "private_key_id": "...",
        "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
        "client_email": "...@project.iam.gserviceaccount.com",
        "client_id": "...",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}'
    auth_scopes:
    - https://www.googleapis.com/auth/bigquery
    - https://www.googleapis.com/auth/cloud-platform
    - https://www.googleapis.com/auth/drive
    dataset: sodasql
```

Alternatively, use the `env_vars.yml` file to securely store the service account's JSON connection credentials. See [Env_vars YAML file](/docs/soda-sql/warehouse.md#env_vars-yaml-file) for details.

```yaml
name: my_bigquery_project
connection:
    type: bigquery
    account_info_json: env_var(BIG_QUERY_ACCESS)
    auth_scopes:
    - https://www.googleapis.com/auth/bigquery
    - https://www.googleapis.com/auth/cloud-platform
    - https://www.googleapis.com/auth/drive
    dataset: sodasql
```

Alternatively, you can specify Big Query configuration using the `account_info_json_path` configuration option to direct Soda SQL to your Big Query service account JSON key file.

```yaml
name: my_bigquery_project
connection:
    type: bigquery
    account_info_json_path: /folder/service-account-file.json
    auth_scopes:
    - https://www.googleapis.com/auth/bigquery
    - https://www.googleapis.com/auth/cloud-platform
    - https://www.googleapis.com/auth/drive
    dataset: sodasql
```

Alternatively, you can specify Big Query configuration using the `use_context_auth` configuration option to direct Soda SQL to your Big Query global environnement variable `(GOOGLE_APPLICATIONS_CREDENTIALS)`.

```yaml
name: my_bigquery_project
connection:
    type: bigquery
    use_context_auth: true
    project_id: your_project_id
    auth_scopes:
    - https://www.googleapis.com/auth/bigquery
    - https://www.googleapis.com/auth/cloud-platform
    - https://www.googleapis.com/auth/drive
    dataset: sodasql
```


| Property |  Required | 
| -------- |  -------- | 
| type | required | 
| project_id | required | 
| private_key_id | required |
| private_key | required |
| client_email | required |
| client_id | required |
| auth_uri | required |
| token_uri | required |
| auth_provider_x509_cert_url | required |
| client_x509_cert_url | required | 
| auth_scopes | optional; Soda applies the three scopes listed above by default |
| dataset | required |

### Big Query permissions

To run Soda scans of your data in Big Query, you must configure some permissions in the Big Query Service Account. 

1. In the Google Cloud Platform, make sure that you are in the Project that contains the Service Account you will use to access your Big Query dataset. Navigate to **Service Accounts** to confirm that you see an expected list of Service Accounts.
2. Access **Roles**, then create a new role named "BigQuery Soda Scan User" that includes the permissions listed below. Alternatively, you can add these permissions to an existing role to which the Service Account is associated, if you prefer.
* bigquery.jobs.create
* bigquery.tables.get
* bigquery.tables.getData
* bigquery.tables.list 

3. Access **IAM** > **Permissions** and, to the service account that you will use to access your Big Query dataset, add the following the following roles:
* BigQuery Data Viewer
* BigQuery Read Session User
* BigQuery Soda Scan User
4. After saving your changes to the Service Account, complete the steps to [configure Soda SQL](/docs/soda-sql/configure.md) and run your first scan.

The Google Cloud Platform offers more granular control of user access to data in Big Query. If you wish to further refine the data to which Service Accounts have access, refer to the Google Cloud Platform documentation. 
* <a href="https://cloud.google.com/bigquery/docs/row-level-security-intro" target="_blank">Introduction to BigQuery row-level security </a>
* <a href="https://cloud.google.com/bigquery/docs/column-level-security-intro" target="_blank">Introduction to BigQuery column-level security </a>
* <a href="https://cloud.google.com/bigquery/docs/table-access-controls-intro?hl=en" target="_blank">Introduction to table access controls </a>
* <a href="https://cloud.google.com/bigquery/docs/dataset-access-controls?hl=en" target="_blank"> Controlling access to datasets </a>


## Microsoft SQL Server (Experimental)

Note: MS SQL Server support is experimental.


```yaml
name: my_sqlserver_project
connection:
  type: sqlserver
  host: <YOUR SQLServer HOSTNAME>
  username: env_var(SQL_SERVER_USERNAME)
  password: env_var(SQL_SERVER_PASSWORD)
  database: master
  schema: dbo
```

| Property |  Required | Notes |
| -------- |  -------- | ----- |
| type | required |  |
| host| required |  |
| username| required | Use environment variables to retrieve this value securely. |
| password| required | Use environment variables to retrieve this value securely. |
| database| required |  |
| schema | required | |


## MySQL (Experimental)

Note: MySQL support is in a very early experimental stage.

```yaml
name: my_sqlserver_project
connection:
  type: mysql
  host: localhost
  username: sodasql
  password: sodasql
  database: sodasql
```

| Property |  Required | Notes |
| -------- |  -------- | ----- |
| type | required |  |
| host| required |  |
| username| required | Use environment variables to retrieve this value securely. |
| password| required | Use environment variables to retrieve this value securely. |
| database| required |  |

## PostgreSQL

```yaml
name: my_postgres_project
connection:
    type: postgres
    host: localhost
    port: '5432'
    username: sodasql
    password: sodasql
    database: sodasql
    schema: public
...
```

| Property |  Required | Notes |
| -------- |  -------- | ----- |
| type | required |  |
| host| required |  |
| port | optional |  |
| username| required | Use environment variables to retrieve this value securely. |
| password| required | Use environment variables to retrieve this value securely. |
| database| required |  |
| schema | required | |

## Snowflake

```yaml
name: my_snowflake_project
connection:
    type: snowflake
    username: env_var(SNOWFLAKE_USERNAME)
    password: 
    database: 
    schema: PUBLIC
    role: PUBLIC
    passcode_in_password:
    private_key_passphrase: 
    private_key: 
    private_key_path: '/path/to/private_key/key.p8'
    authenticator: snowflake
session_parameters:
    QUERY_TAG: soda-queries
    QUOTED_IDENTIFIERS_IGNORE_CASE: false
```

| Property | Required | Notes |
| --------  | -------- | -----|
| type  | required |  The name of your Snowflake virtual warehouse. |
| username | required | Use environment variables to retrieve this value securely. |
| password | optional | Use environment variables to retrieve this value securely using `env_var(SNOWFLAKE_PASSWORD)`. Alternatively, authenticate using `private_key`, `private_key_passphrase`, or `private-key-path`. |
| database | optional |  |
| schema | required |  |
| role | optional | See <a href="https://docs.snowflake.com/en/user-guide/security-access-control-overview.html#system-defined-roles" target="_blank">Snowflake System-Defined Roles</a> for details.|
| passcode_in_password | optional | Default value is `false`. See <a href="https://docs.snowflake.com/en/user-guide/snowsql-start.html#mfa-passcode-in-password" target="_blank"> Snowflake documentation</a>.|
| private_key_passphrase | optional | Specify the value for the key-value pair. |
| private_key | optional | See [Private key authentication](#private-key-authentication) section below.|
| private_key_path | optional | Example: `private_key_path: '/path/to/private_key/key.p8'` |
| authenticator | optional | Default value is `snowflake`. See <a href="https://docs.snowflake.com/en/user-guide/snowsql-start.html#authenticator" target="_blank"> Snowflake documentation</a>. |
| QUERY_TAG | optional | See <a href="https://docs.snowflake.com/en/sql-reference/parameters.html#query-tag" target="_blank">QUERY_TAG</a> in Snowflake documentation. |
| QUOTED_IDENTIFIERS_IGNORE_CASE | optional | See <a href="https://docs.snowflake.com/en/sql-reference/parameters.html#quoted-identifiers-ignore-case" target="_blank">QUOTED_IDENTIFIERS_IGNORE_CASE</a> in Snowflake documentation. |


### Private key authentication

You can use the `private_key` parameter to specify key-value pairs for key pair authentication. In the warehouse YAML file, add the parameter as follows: 
```yml
  private_key: |
     -----BEGIN ENCRYPTED PRIVATE KEY-----
     MIIExxxxxxxxxxxxxxxxxxxxucRqSZaS
     ...

     -----END ENCRYPTED PRIVATE KEY-----
```

## Trino (Experimental)

```yaml
name: my_trino_project
connection:
    type: trino
    host: localhost
    port: '443'
    http_scheme: 'https'
    catalog: your_catalog
    schema: your_database
    username: 
    password: 

...
```

| Property |  Required | Notes |
| -------- |  -------- | ----- |
| type     | required |        |
| host     | required |        |
| port     | required |        |
| http_scheme | https |        |
| catalog  | required | The name of your catalog.  |
| schema   | required | The name of your database. |
| username | required | Use environment variables to retrieve this value securely. |
| password | required | Use environment variables to retrieve this value securely. |


<br />
