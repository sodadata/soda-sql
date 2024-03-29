from typing import List

from tests.common.warehouse_fixture import WarehouseFixture


class SparkFixture(WarehouseFixture):

    def create_database(self):
        pass

    def drop_database(self):
        pass

    def tear_down(self):
        pass

    def sql_create_table(self, columns: List[str], table_name: str):
        columns_sql = ", ".join(columns)
        return f"CREATE TABLE " \
               f"{self.warehouse.dialect.qualify_writable_table_name(table_name)} ( \n " \
               f"{columns_sql} )"

    def test_warehouse_connection(self):
        assert(self.warehouse.dialect.sql_test_connection())
