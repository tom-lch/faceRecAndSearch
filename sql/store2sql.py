import pymysql
import re
import time


class FaceaiMySQL:

      def __init__(self, host="localhost", port="3306", user="root", pwd="123456", dbname="faceai", tables=["",]):
            self.host = host
            self.port = port
            self.user = user
            self.pwd = pwd
            self.dbname = dbname
            self.tables = tables
            self.DB = self._connect_sql()
            self.cursor = self.DB.cursor()
            self._db_exists(dbname)
            for table in tables:
                  self._table_exists(table)
            # 开一个线程保持对mysql的连接 不可直调用。
            # self._activate()

      def _connect_sql(self):
            return pymysql.connect(self.host, self.user, self.pwd, self.dbname, self.port)

      def _db_exists(self, dbname):
            sql = "show databases"
            self.cursor.execute(sql)
            databases = [self.cursor.fetchall()]
            databases_list = re.findall('(\'.*?\')',str(databases))
            databases_list = [re.sub("'",'',each)for each in databases_list]
            if dbname in databases_list:
                  return 
            else:
                  sql = "CREATE DATABASE IF NOT EXISTS " + dbname
                  try:
                        self.cursor.execute(sql)
                        self.DB.commit()
                        print("Successfully added database")
                  except:
                        self.DB.rollback()
                        print("UNSuccessfully added database")

      def _table_exists(self, table):
            sql = "show tables"
            self.cursor.execute(sql)
            tables = self.cursor.fetchall()
            tables_list = re.findall('(\'.*?\')',str(tables))
            # print(tables_list)
            tables_list = [re.sub("'",'',each)for each in tables_list]
            # print(tables_list)
            if table in tables_list:
                  return True
            else:
                  print("table not exists")
                  try :
                        self._createTable(table)
                        print("Successfully added table")
                  except:
                        self.DB.rollback()
                        print("UnSuccessfully added table")

      def _createTable(self, table):
            sql = f"create table if not exists `{table}` (`id` int auto_increment primary key, `img_info_id` VARCHAR(20),`img_path` VARCHAR(64),`img_url` VARCHAR(256), `img_location` VARCHAR(64), `photo_web` VARCHAR(64))character set utf8;"
            self._get_conn()
            self.cursor.execute(sql)
            self.DB.commit()

      def InsertImage(self, table, img_info_id, img_path, img_url, img_location, photo_web):
            sql = f"INSERT INTO {table}(img_info_id,img_path, img_url, img_location, photo_web) VALUES ('{img_info_id}', '{img_path}', '{img_url}', '{img_location}', '{photo_web}')"
            try:  
                  print(sql)
                  self._get_conn()
                  self.cursor.execute(sql)
                  # 提交到数据库执行
                  self.DB.commit()
                  print("insert success")
                  return self.cursor.lastrowid, True
            except:
                  self.DB.rollback()
                  print("error:  insert unsuccess")
                  return 0, False

      def SearchImage(self, table, img_id, img_info_id):
            if img_info_id: 
                  sql = f"SELECT * FROM {table} WHERE img_info_id={img_info_id};"
            if img_id:
                  sql = f"SELECT * FROM {table} WHERE id={img_id};"
            try:
                  self._get_conn()
                  self.cursor.execute(sql)
                  # 提交到数据库执行
                  results = self.cursor.fetchall()
                  # print(results)
                  return results[0]
            except:
                  return []

      def UpdateImage(self, table, img_path, img_url, img_location, img_info_id, photo_web):            
            sql = f"""
                  UPDATE {table} SET img_path {img_path}, img_url {img_url},  img_location {img_location}, photo_web {photo_web} WHERE img_info_id={img_info_id};
            """
            try:
                  self._get_conn()
                  self.cursor.execute(sql)
                  # 提交到数据库执行
                  self.DB.commit()
                  print("insert success")
            except:
                  self.DB.rollback()

      def DeleteImage(self, table, img_id):
            if img_id:
                  sql = f"DELETE FROM {table} WHERE id={img_id}"
            try:
                  self._get_conn()
                  self.cursor.execute(sql)
                  # 提交到数据库执行
                  self.DB.commit()
                  print("insert success")
            except:
                  self.DB.rollback()

      def _get_conn(self):
            if self.DB is not None:
                  try:
                        self.DB.ping(True)
                        return 
                  except Exception as e:
                        logging.exception(e)
            try:
                  self.DB = self._connect_sql()
                  self.cursor = self.DB.cursor()
                  return
            except Exception as e:
                  logging.exception(e)

