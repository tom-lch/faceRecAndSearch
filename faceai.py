from flask import Flask, jsonify, request, redirect
from logic import searchFromMilvus, GetImageArr, faceDetAndEncodingToSQL, detectionFace, EncodingFace, detectionAndEncodingFace

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



if __name__ == "__main__":
      app.run(host = "0.0.0.0",port=8802)