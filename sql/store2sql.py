import pymysql

class FaceaiMySQL:

      def __init__(self, host="127.0.0.1", port="3306", user="root", pwd="123456", dbname="faceai", tables=["faceai",]):
            self.DB = _connect_sql(host, user, pwd, dbname)
            self.cursor = self.DB.cursor()
            _db_exists(dbname)
            for table in tables:
                  _table_exists(table)

      def _connect_sql(self, host, user, pwd, dbname):
            return pymysql.connect(host, user, pwd, dbname)

      def _db_exists(self, dbname):
            sql = "show databases"
            self.cursor.execute(sql)
            databases = [self.cursor.fetchall()]
            databases_list = re.findall('(\'.*?\')',str(databases))
            # print(databases_list)
            databases_list = [re.sub("'",'',each)for each in databases_list]
            if dbname in databases_list:
                  return 
            else:
                  sql = "CREATE DATABASE IF NOT EXISTS " + dbname
                  try:
                        cursor.execute(sql)
                        db.commit()
                        print("Successfully added database")
                  except:
                        db.rollback()
                        print("Successfully added database")

      def _table_exists(self , table):
            sql = "show tables"
            cursor.execute(sql)
            tables = cursor.fetchall()
            # print(tables)
            tables_list = re.findall('(\'.*?\')',str(tables))
            # print(tables_list)
            tables_list = [re.sub("'",'',each)for each in tables_list]
            # print(tables_list)
            if table in tables_list:
                  return True
            else:
                  print("table not exists")
                  try :
                        _createTable(table)
                  except:
                        db.rollback()
                        print("UnSuccessfully added table")

      def _createTable(self, table):
            sql = f"""CREATE TABLE {table} (
            img_id  INT UNSIGNED AUTO_INCREMENT,
            img_info_id  VARCHAR(20) UNIQUE,
            img_path  VARCHAR(64),
            img_url  VARCHAR(64),  
            img_location VARCHAR(64),
            PRIMARY KEY ( img_ingo_id )
            )"""
            cursor.execute(sql)

      def InsertImage(self, table, img_info_id, img_path, img_url, img_location):
            sql = f"""INSERT INTO {table}(img_info_id,
                  img_path, img_url, img_location)
                  VALUES ({img_info_id}, {img_path}, {img_url}, {img_location})"""
            try:
                  self.cursor.execute(sql)
                  # 提交到数据库执行
                  self.DB.commit()
                  print("insert success")
            except:
                  self.DB.rollback()

      def SearchImage(self, table, img_info_id):
            sql = f"SELECT * FROM {table} WHERE img_info_id={img_info_id}"
            try:
                  self.cursor.execute(sql)
                  # 提交到数据库执行
                  results = cursor.fetchall()
                  return resluts
            except:
                  return []

      def UpdateImage(self, table, img_path, img_url, img_location, img_info_id):            
            sql = f"""
                  UPDATE {table} SET img_path {img_path}, img_url {img_url},  img_location {img_location} WHERE img_info_id={img_info_id}
            """
            try:
                  self.cursor.execute(sql)
                  # 提交到数据库执行
                  self.DB.commit()
                  print("insert success")
            except:
                  self.DB.rollback()

      def DeleteImage(self, table, img_info_id):
            sql = f"DELETE FROM {table} WHERE img_info_id={img_info_id}"
            try:
                  self.cursor.execute(sql)
                  # 提交到数据库执行
                  self.DB.commit()
                  print("insert success")
            except:
                  self.DB.rollback()

