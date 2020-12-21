from sql import FaceaiMySQL
import logging

# 使用mysql目前存在问题
mysqlClient = FaceaiMySQL(tables=["face_test1", ])

def Store2mysql(table, img_info_id, img_path, img_url, img_location, photoWeb):
      id, bl = mysqlClient.InsertImage(table, img_info_id, img_path, img_url, img_location, photoWeb)
      return id, bl


def SelectInfoFromMySQL(table, imgID, img_info_id):
      res = mysqlClient.SearchImage(table, imgID, img_info_id)
      return res



