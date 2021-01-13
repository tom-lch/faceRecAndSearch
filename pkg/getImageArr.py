from PIL import Image
import numpy as np
from pkg import GenName, DownloadImageByUrl
import shutil
import time
import os

def GetImageArr(url):
      # 根据图片URL用于人脸识别
      # 使用生成的名字下载图片在本地
      StorePath = StoreAndDel()
      DownloadImageByUrl(url, StorePath)
      # 从下载好的图片读取信息成 array
      ImageArr = LoadImage2Array(StorePath)
      return ImageArr, StorePath  

def LoadImage2Array(name, mode='RGB'):
      img = Image.open(name)
      if mode:
            img = img.convert(mode)
      return np.array(img)


def StoreAndDel():
      name = GenName() 
      hour = int(time.time()) // 3600
      path = "/apps/Storage/tmp/image/" + str(hour)
      if CreateFolder(path) == 1:
            DeleteFolder("/apps/Storage/tmp/image/" + str(hour-1))
      StorePath = path + "/" + name + ".jpg" # 后期调整成从配置文件读取路径
      return StorePath

def CreateFolder(folder_name):
      result_data = 0
      folder_name_exist = os.path.exists(folder_name)
      if not folder_name_exist:
            os.makedirs(folder_name)
            result_data = 1
      return result_data

def DeleteFolder(path):
      shutil.rmtree(path)