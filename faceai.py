from flask import Flask, jsonify, request, redirect
from logic import SearchFromMilvusByArr, faceDetAndEncodingToSQLAndMilvus, detectionFace, EncodingFace, detectionAndEncodingFace, Delete_collection_from_milvus
from pkg import GetImageArr
from config.cfg import Config
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}



app = Flask(__name__)

@app.route("/faceSearchSample", methods=["POST"])
def FaceSearchSample():
      url = request.form["url"]
      # table = request.form["table"]
      collection_name = Config["milvus"]["collection_name"]
      table = Config["mysql"]["table"]
      imgArr, _ = GetImageArr(url)
      return SearchFromMilvusByArr(imgArr, table, collection_name)

@app.route("/faceDetAndEncodeByURLToSQLAndMilvus", methods=["POST"])
def FaceDetAndEncodeByURLToSQLAndMilvus():
      url = request.form["url"]
      photoWeb = request.form["photoWeb"]
      # table = request.form["table"]
      table = Config["mysql"]["table"]
      collection_name = Config["milvus"]["collection_name"]
      imgArr, imagePath = GetImageArr(url)
      return faceDetAndEncodingToSQLAndMilvus(imgArr, imagePath, url, photoWeb, table, collection_name)


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

@app.route("/deleteSQL", methods=["POST"])
def DeleteSQL():
      name = request.form["name"]
      Delete_collection_from_milvus(name)



if __name__ == "__main__":
      app.run(host = "0.0.0.0",port=8802)