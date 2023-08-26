#encoding=utf-8
from BaseMysql import BaseMysql

class InitDbTable(BaseMysql):
    def __init__(self):
        super().__init__()

    def create_database(self, database_name):
        print("开始创建数据库")
        sql = "CREATE DATABASE IF NOT EXISTS %s" % database_name
        self.execute_sql(sql)

    def create_table_target_user(self):
        print("开始创建表")
        path_sql = "sql/create_table_target_user.sql"
        with open(path_sql, 'r') as f:
            sql = f.read()
            sql = sql.replace("\n", "")
        sql = "use wemedia; CREATE TABLE if not exists table_target_user (platform VARCHAR(100));"
        sql = "use wemedia; create table user (name varchar(23))"
        self.execute_sql(sql)
        


if __name__ == "__main__":
    obj_init_db_table = InitDbTable()
    # obj_init_db_table.create_database("wemedia")
    obj_init_db_table.create_table_target_user()
    obj_init_db_table.close_conn()