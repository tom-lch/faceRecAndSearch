import face_recognition
from flask import jsonify
from .milvus import Store2Milvus, SearchFromMilvus
from .mysql import Store2mysql, SelectInfoFromMySQL
from pkg import GenID
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
            imgInfoID = GenID() # 在这里同样将 img_encoding img_location  imageUrl imagePath 保存到mysql 并返回能检索到的ID
            table = "face_infos"
            id, bl = Store2mysql(table, str(imgInfoID), imagePath, imageUrl, img_location)
            if bl == False :
                  return jsonify({"state": "error mysql插入报错", "ids": None})
            Store2Milvus(id, img_encoding)
            ids[i] = (id, imgInfoID)
      return jsonify({"state": "OK", "ids": ids})


def SearchFromMilvusByArr(ImageArr):
      img_encodings = face_recognition.face_encodings(ImageArr)
      infos = {}
      imageInfos = {}
      idss = []
      for i in range(len(img_encodings)):
            img_encoding = img_encodings[i]
            info = SearchFromMilvus(img_encoding)
            colls = {}
            ids = []
            for val in info:
                  imgID = val["imgID"]
                  ids.append(imgID)
                  # 根据imgID 从mysql中获取图片信息
                  res = SelectInfoFromMySQL("face_infos" ,int(imgID), None)
                  colls[str(imgID)] = res
            infos[str(i)] = info
            imageInfos[str(i)] = colls
            idss.append(ids)
      return jsonify({"infos": infos, "imageInfos": imageInfos, "idss": idss})


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








