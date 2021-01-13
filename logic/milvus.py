from sql import FaceMilvus
from config.cfg import Config


milvusClient = FaceMilvus(host=Config["milvus"]["host"], port=Config["milvus"]["port"], collection_name=Config["milvus"]["collection_name"])

# def NewMilvusCLient(table):
#       globla milvusClient
#       milvusClient = FaceMilvus(collection_name=table)


def Store2Milvus(imgID, imgEncoding, collection_name):
      ids = milvusClient.Insert(imgID, imgEncoding, collection_name)

def SearchFromMilvus(imgEncoding, collection):
      info = milvusClient.Search(imgEncoding, collection)
      return info

def Delete_collection_from_milvus(collection_name):
      milvusClient.Delete(collection_name)


# #milvusClient = FaceMilvus(collection_name='face_test1')


# class MilvusClient:
#       def _init__(self, table):
#             self.milvusClient = FaceMilvus(collection_name=table)

#       def Store2Milvus(self, imgID, imgEncoding):
#             ids = milvusClient.Insert(imgID, imgEncoding)

#       def SearchFromMilvus(self, imgEncoding):
#             info = milvusClient.Search(imgEncoding)
#             return info

#       def Delete_collection_from_milvus(self, collection_name):
#             milvusClient.Delete(collection_name)