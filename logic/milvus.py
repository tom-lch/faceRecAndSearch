from sql import FaceMilvus

milvusClient = FaceMilvus(collection_name='faceai')

def Store2Milvus(imgInfoID, imgEncoding):
      ids = milvusClient.Insert(imgInfoID, imgEncoding)

def SearchFromMilvus(imgEncoding):
      info = milvusClient.Search(imgEncoding)
      return info

def Delete_collection_from_milvus(collection_name):
      milvusClient.Delete(collection_name)