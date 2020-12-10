import face_recognition
from flask import jsonify
from .milvus import Store2Milvus, SearchFromMilvus
import random

def faceDetAndEncodingToSQLAndMilvus(ImageArr, imagePath, imageUrl):
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
            # Store2mysql(imgInfoID, imagePath, imageUrl, img_location)
            id = Store2Milvus(imgInfoID, img_encoding)
            ids[i] = id
      return jsonify({"state": "OK", "ids": ids})


def SearchFromMilvusByArr(ImageArr):
      img_encodings = face_recognition.face_encodings(ImageArr)
      infos = {}
      for i in range(len(img_encodings)):
            img_encoding = img_encodings[i]
            info =  SearchFromMilvus(img_encoding)
            infos[str(i)] = info
      return jsonify({"infos": infos})


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








