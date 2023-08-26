#encoding=utf-8
import pymysql

class BaseMysql(object):
    def __init__(self):
        self.conn = pymysql.connect(host='23.251.54.154', 
                               user='remote', 
                               password='remote'
                               )

        self.cursor = None

    def execute_sql(self, sql):
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql)
        self.conn.commit()

        
    def close_conn(self):
        self.cursor.close()
        self.conn.close()
                               
                               
if __name__=="__main__":
    obj_manu_mysql = BaseMysql()