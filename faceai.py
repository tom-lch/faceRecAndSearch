import face_recognition
from flask import Flask, jsonify, request, redirect
import numpy as np
import requests
from PIL import Image
import time
from pkg import FaceMilvus
import random
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)

@app.route("/faceSearchSample", methods=["POST"])
def FaceSearchSample():
      url = request.form["url"]
      imgArr, _ = GetImageArr(url)
      return searchFromMilvus(imgArr)

@app.route("/faceDetAndEncodeByURLToSQL", methods=["POST"])
def FaceDetAndEncodeByURLToSQL():
      url = request.form["url"]
      imgArr, imagePath = GetImageArr(url)
      return faceDetAndEncodingToSQL(imgArr, imagePath, url)


@app.route("/faceDetByURL", methods=["POST"])
def FaceDetByUrl():
      url = request.form["url"]
      imgArr, _ = GetImageArr(url)
      return detectionFace(imgArr)

# 使用post上传本地图片文件
@app.route("/faceDetByPath", methods=["POST"])
def FaceDetByPath():
      ImgFile = request.files['photoFile']
      imgArr = face_recognition.load_image_file(ImgFile)
      return detectionFace(imgArr)

@app.route("/faceEncodeByURL", methods=["POST"])
def FaceEncodeByURL():
      url = request.form["url"]
      imgArr, _ = GetImageArr(url)
      return EncodingFace(imgArr)

@app.route("/faceDetAndEncodeByURL", methods=["POST"])
def FaceDetAndEncodeByURL():
      url = request.form["url"]
      imgArr, _ = GetImageArr(url)
      return detectionAndEncodingFace(imgArr)

# @app.route("/deleteSQL", methods=["POST"])
# def DeleteSQL():
#       name = request.form["name"]
#       _delete_collection_from_milvus(name)

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
            imgInfoID = i + random.randint(0, 10000)
            id = _Store2Milvus(imgInfoID, img_encoding)
            ids[i] = id
      return jsonify({"state": "OK", "ids": ids})

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


if __name__ == "__main__":
      app.run(host = "0.0.0.0",port=8801)