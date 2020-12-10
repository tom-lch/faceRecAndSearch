import numpy as np
import requests
from PIL import Image
import time
from pkg import FaceMilvus, FaceaiMySQL
import random
import face_recognition
from flask import jsonify, request


def faceDetAndEncodingToSQL(ImageArr, imagePath, imageUrl):
      img_encodings = face_recognition.face_encodings(ImageArr)
      img_locations = face_recognition.face_locations(ImageArr)
      imgs = {}
      ids = {}
      for i in range(len(img_locations)):
            img_encoding = img_encodings[i]
            img_location = str(img_locations[i])[1:-1]
            # store2milvus 存入数据库
            # 需要修改： 由于Milvus目前不支持存储string类型，需要将string存储到另外的数据库中，将该ID传入milvus
            # imgInfoID = storeImageImfo(imagePath, imageUrl, img_location)
            imgInfoID = i + random.randint(0, 10000)  # 在这里同样将 img_encoding img_location  imageUrl imagePath 保存到mysql 并返回能检索到的ID
            store2mysql(imgInfoID, imagePath, imageUrl, img_location)
            id = _Store2Milvus(imgInfoID, img_encoding)
            ids[i] = id
      return jsonify({"state": "OK", "ids": ids})

def GenUUID():
      return str(uuid.uuid4())

def searchFromMilvus(ImageArr):
      img_encodings = face_recognition.face_encodings(ImageArr)
      infos = {}
      for i in range(len(img_encodings)):
            img_encoding = img_encodings[i]
            info =  _SearchFromMilvus(img_encoding)
            infos[str(i)] = info
      return jsonify({"infos": infos})

milvusClient = FaceMilvus(collection_name='faceai')

def _Store2Milvus(imgInfoID, imgEncoding):
      ids = milvusClient.Insert(imgInfoID, imgEncoding)

def _SearchFromMilvus(imgEncoding):
      info = milvusClient.Search(imgEncoding)
      return info

def _delete_collection_from_milvus(collection_name):
      milvusClient.Delete(collection_name)

# 使用mysql目前存在问题
# mysqlClient = FaceaiMySQL(host="127.0.0.1", port="3306", user="root", pwd="123456", dbname="faceai", tables=["faceai",])

# def store2mysql(table="faceai", img_info_id, img_path, img_url, img_location):
#       mysqlClient.InsertImage(table, img_info_id, img_path, img_url, img_location)

def detectionAndEncodingFace(ImageArr):
      img_encodings   = face_recognition.face_encodings(ImageArr)
      img_locations = face_recognition.face_locations(ImageArr)
      imgs = {}
      for i in range(len(img_locations)):
            images = {}
            images["img_encodings"] = str(img_encodings[i]).replace("\n", "")[1:-1]
            images["img_locations"] = str(img_locations[i])[1:-1]
            imgs[str(i)] = images
      # print(type(img_encoding), img_encoding)
      return jsonify({"img":imgs})

def EncodingFace(ImageArr):
      img_encodings = face_recognition.face_encodings(ImageArr)
      imgs = {}
      for i in range(len(img_encodings)):
            images = {}
            images["img_encodings"] = str(img_encodings[i]).replace("\n", "")[1:-1]
            imgs[str(i)] = images
      return jsonify({"img":imgs})

def detectionFace(ImageArr):
      img_locations = face_recognition.face_locations(ImageArr)
      imgs = {}
      for i in range(len(img_locations)):
            images = {}
            images["img_locations"] = str(img_locations[i])[1:-1]
            imgs[str(i)] = images
      # print(type(img_encoding), img_encoding)
      return jsonify({"img":imgs})

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

def DownloadImageByUrl(url, name):
      resp = requests.get(url)
      with open(name, "wb") as f:
            f.write(resp.content)

def GenName():
      # 生成随机名字
      pre = time.time()
      name = str(int(round(pre * 1000)))
      return name
