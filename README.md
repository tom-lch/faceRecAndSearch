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
curl --data "url=http://upload.mnw.cn/2020/0922/1600761074390.jpg" localhost:8802/faceEncodeByURL

# 将人脸编码存入milvus
curl --data "url=http://upload.mnw.cn/2020/0922/1600761074390.jpg" localhost:8802/faceDetAndEncodeByURLToSQL

# 查询相似
curl --data "url=http://upload.mnw.cn/2020/0922/1600761074390.jpg" localhost:8802/faceSearchSample

# 删除创建的人脸相似表
curl --data 'name=faceai' localhost:8801/deleteSQL
```

验证milvus是否安装成功
```
python example.py
```