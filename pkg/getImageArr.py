from PIL import Image
import numpy as np
from pkg import GenName, DownloadImageByUrl


def GetImageArr(url):
      # 根据图片URL用于人脸识别
      # 使用生成的名字下载图片在本地
      name = GenName() 
      StorePath = "./image/" + name + ".jpg" # 后期调整成从配置文件读取路径
      DownloadImageByUrl(url, StorePath)
      # 从下载好的图片读取信息成 array
      ImageArr = LoadImage2Array(StorePath)
      return ImageArr, StorePath  

def LoadImage2Array(name, mode='RGB'):
      img = Image.open(name)
      if mode:
            img = img.convert(mode)
      return np.array(img)