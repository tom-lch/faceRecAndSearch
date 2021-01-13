from sql import FaceaiMySQL
import logging
from config.cfg import Config
# 使用mysql目前存在问题
mysqlClient = FaceaiMySQL(host=Config["mysql"]["host"], 
                        port=Config["mysql"]["port"], 
                        user=Config["mysql"]["user"], 
                        pwd=Config["mysql"]["pwd"],
                        dbname=Config["mysql"]["dbname"], 
                        tables=Config["mysql"]["tables"])

def Store2mysql(table, img_info_id, img_path, img_url, img_location, photoWeb):
      id, bl = mysqlClient.InsertImage(table, img_info_id, img_path, img_url, img_location, photoWeb)
      return id, bl


def SelectInfoFromMySQL(table, imgID, img_info_id):
      res = mysqlClient.SearchImage(table, imgID, img_info_id)
      return res


if __name__ == '__main__':
      print(mysqlClient)


