# 关于使用

```
# 启动web端
python faceai.pi
```

使用curl调用服务验证API

```
# 获取人脸框
curl --data "url=http://upload.mnw.cn/2020/0922/1600761074390.jpg" localhost:8802/faceDetByURL

# 获取人脸编码
curl --data "url=http://upload.mnw.cn/2020/0922/1600761074390.jpg" localhost:8802/faceEncodeByUR

# 将人脸编码存入 SQL And Milvus
curl --data "url=http://upload.mnw.cn/2020/0922/1600761074390.jpg" localhost:8802/faceDetAndEncodeByURLToSQLAndMilvus

# 查询相似
curl --data "url=http://upload.mnw.cn/2020/0922/1600761074390.jpg" localhost:8802/faceSearchSample
curl --data "url=http://p5.itc.cn/images01/20200922/b43039d895024a8e8a9c6d1c091301eb.jpeg" localhost:8802/faceSearchSample
# 删除创建的人脸相似表
curl --data 'name=faceai' localhost:8801/deleteSQL
```

验证milvus是否安装成功
```
python example.py
```

![WangBingbing][./image/1607664239160.jpg]