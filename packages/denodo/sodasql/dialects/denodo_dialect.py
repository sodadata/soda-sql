#  Copyright 2020 Soda
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import logging
from typing import Optional

import psycopg2
from sodasql.scan.dialect import Dialect, DENODO, KEY_WAREHOUSE_TYPE
from sodasql.scan.parser import Parser

logger = logging.getLogger(__name__)


class DenodoDialect(Dialect):

    def __init__(self, parser: Parser = None, type: str = DENODO):
        super().__init__(type)
        if parser:
            self.host = parser.get_str_optional_env('host', 'localhost')
            self.port = parser.get_str_optional_env('port', '9996')
            self.username = parser.get_str_required_env('username')
            self.password = parser.get_credential('password')
            self.database = parser.get_str_required_env('database')

    def default_connection_properties(self, params: dict):
        return {
            KEY_WAREHOUSE_TYPE: DENODO,
            'host': 'localhost',
            'port': '9996',
            'username': 'env_var(DENODO_USERNAME)',
            'password': 'env_var(DENODO_PASSWORD)',
            'database': params.get('database', 'your_database'),

        }

    def get_warehouse_name_and_schema(self) -> dict:
        return {
            'database_name': self.database,
            'database_schema': self.schema
        }

    def safe_connection_data(self):
        return [
            self.type,
            self.host,
            self.port,
            self.database,
        ]

    def default_env_vars(self, params: dict):
        return {
            'DENODO_USERNAME': params.get('username', 'Eg johndoe'),
            'DENODO_PASSWORD': params.get('password', 'Eg abc123')
        }

    def create_connection(self):
        try:
            conn = psycopg2.connect(
                user=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database)
            return conn
        except Exception as e:
            self.try_to_raise_soda_sql_exception(e)

    def query_table(self, table_name):

        query = f"""
        SELECT *
        FROM {table_name}
        LIMIT 1
        """
        return query

    def sql_test_connection(self) -> bool:
        return True

    def sql_columns_metadata_query(self, table_name: str) -> str:
        sql = (f"SELECT column_name, data_type, is_nullable \n"
               f"FROM information_schema.columns \n"
               f"WHERE lower(table_name) = '{table_name}'")
        if self.database:
            sql += f" \n  AND table_catalog = '{self.database}'"
        if self.schema:
            sql += f" \n  AND table_schema = '{self.schema}'"
        return sql

    def is_text(self, column_type: str):
        return column_type.upper() in ['CHARACTER VARYING', 'CHARACTER', 'CHAR', 'TEXT']

    def is_number(self, column_type: str):
        return column_type.upper() in ['SMALLINT', 'INTEGER', 'BIGINT', 'DECIMAL', 'NUMERIC',
                                       'REAL', 'DOUBLE PRECISION', 'SMALLSERIAL', 'SERIAL', 'BIGSERIAL']

    def is_time(self, column_type: str):
        return column_type.upper() in [
            'TIMESTAMP', 'DATE', 'TIME',
            'TIMESTAMP WITH TIME ZONE', 'TIMESTAMP WITHOUT TIME ZONE',
            'TIME WITH TIME ZONE', 'TIME WITHOUT TIME ZONE']

    def qualify_table_name(self, table_name: str) -> str:
        if self.database:
            return f'"{self.database}"."{table_name}"'
        return f'"{table_name}"'

    def qualify_column_name(self, column_name: str, source_type: str = None):
        return f'"{column_name}"'

    def sql_expr_regexp_like(self, expr: str, pattern: str):
        return f"{expr} ~* '{self.qualify_regex(pattern)}'"

    def sql_expr_cast_text_to_number(self, quoted_column_name, validity_format):
        if validity_format == 'number_whole':
            return f"CAST({quoted_column_name} AS {self.data_type_decimal})"
        not_number_pattern = self.qualify_regex(r"[^-\d\.\,]")
        comma_pattern = self.qualify_regex(r"\,")
        return f"CAST(REGEXP_REPLACE(REGEXP_REPLACE({quoted_column_name}, '{not_number_pattern}', '', 'g'), " \
               f"'{comma_pattern}', '.', 'g') AS {self.data_type_decimal})"

    def sql_tables_metadata_query(self, limit: Optional[int] = None, filter: str = None):
        sql = (f"SELECT table_name \n"
               f"FROM information_schema.tables \n"
               f"WHERE lower(table_schema)='{self.database.lower()}'")
        if limit is not None:
            sql += f"\n LIMIT {limit}"
        return sql

    def sql_columns_metadata_query(self, table_name: str) -> str:
        sql = (f"SELECT column_name, data_type, is_nullable \n"
               f"FROM information_schema.columns \n"
               f"WHERE lower(table_name) = '{table_name}'")
        if self.database:
            sql += f" \n  AND table_catalog = '{self.database}'"

        return sql

    def sql_expr_length(self, expr, column: str):
        return f'LEN({expr})'



