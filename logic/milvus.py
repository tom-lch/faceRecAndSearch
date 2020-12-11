from sql import FaceMilvus

milvusClient = FaceMilvus(collection_name='face_infos')

def Store2Milvus(imgID, imgEncoding):
      ids = milvusClient.Insert(imgID, imgEncoding)

def SearchFromMilvus(imgEncoding):
      info = milvusClient.Search(imgEncoding)
      return info

def Delete_collection_from_milvus(collection_name):
      milvusClient.Delete(collection_name)