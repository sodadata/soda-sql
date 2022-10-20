# Developer cookbook

This document describes all the procedures that developers need to know to 
contribute effectively to the Soda SQL codebase.

## Scripts

In directory `scripts` there are a number of convenience scripts that also 
serve as documentation for developer recipes.  So you might want to check there 
if you're looking for how to complete a particular procedure.  They are typically 
created on a mac and may not be compatible on other developer systems.

## Get started with a virtual environment

To get started you need a virtual environment.  Use the following script 
to (re)create a `.venv` virtual environment in the root of the project. 

```
scripts/recreate_venv.sh
```

## Run the pre-commit test suite

Before pushing a commit, be sure to run the pre commit test suite.
The test suite is (and should be) kept fast enough (<2 mins) so that 
it doesn't interrupt the developer flow too much. You can use the script 

```
scripts/run_tests.sh
```

The pre commit test suite requires a local PostgreSQL database 
running with certain user and database preconfigured. Use 
`scripts/start_postgres_container.sh` to start a docker container to 
launch a correct PostgreSQL db with the right user and database.

## Push a release

Make sure that you install dev-requirements
```shell
pip-compile dev-requirements.in
pip install -r dev-requirements.txt
```

Pushing a release is fully automated and only requires to bump the version using `tbump`. For example to release 2.1.0b3, you can use the following command:

```shell
tbump 2.1.0b3
```

### Warehouse dialect

The warehouse dialect defines two things: 

1. **dialect methods** specific to the SQL dialect. This includes methods such as:
   - `is_text` and `is_number` for detecting the data types
   - `sql_tables_metadata_query` and `sql_columns_metadata_query` for 
   fetching metadata
   - `qualify_table_name` and `qualify_column_name` for the table and column
     name
   - `sql_expr_` for some sql expressions
2. **warehouse connection** that the connection engine creates with `create_connection`. The
   connection engine must be compatible with
   [Python database API](https://www.python.org/dev/peps/pep-0249/).
   The connection has two helper methods: `is_connection_error`
   and `is_authentication_error`.

For reference, see the 
[base dialect class](core/sodasql/scan/dialect.py) and the
[Postgres dialect](packages/postgresql/sodasql/dialect.py).


## Add a new warehouse dialect

Take the following steps to add a warehouse dialect:
1. Create a docker container containing a warehouse. For example, 
   [this Docker compose](tests/postgres_container/docker-compose.yml) contains
   the Docker container for the **postgres** warehouse.
2. Add the warehouse `config`, `suite` and `fixture` to the [warehouse tests](tests/warehouses)
   - `config`: is the `warehouse.yml` configuration. Name the file
   `<warehouse>_cfg.yml`. For example, the Postgres configuration is 
     [`postgres_cfg.yml`](tests/warehouses/postgres_cfg.yml)
   - `suite`: contains the setup for the warehouse test suite. Name the file
   `<warehouse>_suite.py`. For example, the Postgres suite is
     [`postgres_suite.py`](tests/warehouses/postgres_suite.py)
   - `fixture`: is the fixture for the warehouse tests. Name the file
   `<warehouse_fixture.py`. For example, the Postgres fixture is
     [`postgres_fixture.py`](tests/warehouses/postgres_fixture.py)
3. Add the `fixture` to the 
  [general warehouse fixture](tests/common/warehouse_fixture.py). 
4. Add the warehouse dialect under [`packages`](packages):
   - `setup.py` : setup to install the dialect.
   - `sodasql/dialects/<warehouse>_dialect.py`: the [warehouse
     dialect](#warehouse-dialect).
  For example the [postgres dialect](packages/postgresql).
5. Add the dialect to [dialect.py](core/sodasql/scan/dialect.py).
6. Add the dialect to [`requirements.txt`](requirements.txt)
