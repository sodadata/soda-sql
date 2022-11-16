# Data types

Soda SQL supports the following data types in columns it scans. 
Currently, Soda does *not* support complex data types.


[Amazon Athena](#amazon-athena) 
[Amazon Redshift](#amazon-redshift) 
[Apache Hive (Experimental)](#apache-hive-experimental) 
[Apache Spark](#apache-spark) 
[Google Cloud Platform Big Query](#google-cloud-platform-big-query) 
[Microsoft SQL Server (Experimental)](#microsoft-sql-server-experimental) 
[MySQL (Experimental)](#mysql-experimental) 
[Postgres](#postgres) 
[Snowflake](#snowflake) 
[Trino (Experimental)](#trino-experimental)
<br />

### Amazon Athena

| Category | Data type | 
| ---- | --------- |
| text | CHAR, VARCHAR, STRING |
| number | TINYINT, SMALLINT, INT, INTEGER, BIGINT, DOUBLE, FLOAT, DECIMAL |
| time | DATE, TIMESTAMP |

### Amazon Redshift

| Category | Data type | 
| ---- | --------- |
| text | CHARACTER VARYING, CHARACTER, CHAR, TEXT, NCHAR, NVARCHAR, BPCHAR |
| number | SMALLINT, INT2, INTEGER, INT, INT4, BIGINT, INT8 |
| time | DATE, TIME, TIMETZ, TIMESTAMP, TIMESTAMPTZ |

### Apache Hive (Experimental)

| Category | Data type | 
| ---- | --------- |
| text | CHAR, VARCHAR |
| number | TINYINT, SMALLINT, INT, BIGINT, FLOAT, DOUBLE, DOUBLE PRECISION, DECIMAL, NUMERIC |

### Apache Spark

| Category | Data type | 
| ---- | --------- |
| text | CHAR, STRING, VARCHAR |
| number | TINYINT, SHORT, SMALLINT, INT, INTEGER, LONG, BIGINT, FLOAT, REAL, DOUBLE, DEC, DECIMAL, NUMERIC |
| time | DATE, TIMESTAMP |

### Google Cloud Platform Big Query

A note about BigQuery datasets: Google uses the term dataset slightly differently than Soda (and many others) do. 
* In the context of Soda, a dataset is a representation of a tabular data structure with rows and columns. A dataset can take the form of a table in PostgreSQL or Snowflake, a stream in Kafka, or a DataFrame in a Spark application. 
* In the context of BigQuery, a <a href="https://cloud.google.com/bigquery/docs/datasets-intro" target="_blank"> dataset</a> is "a top-level container that is used to organize and control access to your tables and views. A table or view must belong to a dataset..."

Instances of "dataset" in Soda documentation always reference the former.

| Category | Data type | 
| ---- | --------- |
| text | STRING |
| number | INT64, DECIMAL, BINUMERIC, BIGDECIMAL, FLOAT64 |
| time | DATE, DATETIME, TIME, TIMESTAMP |

### Microsoft SQL Server

| Category | Data type | 
| ---- | --------- |
| text | VARCHAR, CHAR, TEXT, NVARCHAR, NCHAR, NTEXT |
| number | BIGINT, NUMERIC, BIT, SMALLINT, DECIMAL, SMALLMONEY, INT, TINYINT, MONEY, FLOAT, REAL |
| time | DATE, DATETIMEOFFSET, DATETIME2, SMALLDATETIME, DATETIME, TIME |

### MySQL (Experimental)

| Category | Data type | 
| ---- | --------- |
| text | CHAR, VARCHAR, BINARY, VARBINARY, BLOB, TEXT, ENUM, SET |
| number | INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT, DECIMAL, NUMERIC, FLOAT, DOUBLE, REAL, DOUBLE PRECISION, DEC, FIXED |
| time | TIMESTAMP, DATE, DATETIME, YEAR, TIME |

### Postgres

| Category | Data type | 
| ---- | --------- |
| text | CHARACTER VARYING, CHARACTER, CHAR, TEXT |
| number | SMALLINT, INTEGER, BIGINT, DECIMAL, NUMERIC, VARIABLE, REAL, DOUBLE PRECISION, SMALLSERIAL, SERIAL, BIGSERIAL |
| time | TIMESTAMPT, DATE, TIME, TIMESTAMP WITH TIME ZONE, TIMESTAMP WITHOUT TIME ZONE, TIME WITH TIME ZONE, TIME WITHOUT TIME ZONE |

### Snowflake

| Category | Data type | 
| ---- | --------- |
| text | CHAR, VARCHAR, CHARACTER, STRING, TEXT |
| number | NUMBER, INT, INTEGER, BIGINT, SMALLINT, TINYINT, BYTEINT, FLOAT, FLOAT4, FLOAT8, DOUBLE, DOUBLE PRECISION, REAL |
| time | DATE, DATETIME, TIME, TIMESTAMP, TIMESTAMPT_LTZ, TIMESTAMP_NTZ, TIMESTAMP_TZ |

### Trino (Experimental)

| Category | Data type | 
| ---- | --------- |
| text | VARCHAR, CHAR, VARBINARY, JSON  |
| number | BOOLEAN, INT, INTEGER, BIGINT, SMALLINT, TINYINT, BYTEINT, DOUBLE, REAL, DECIMAL |
| time | DATE, TIME, TIMESTAMP, TIME WITH TIME ZONE, INTERVAL YEAR TO MONTH, INTERVAL DATE TO SECOND |

<br />
