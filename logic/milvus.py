from sql import FaceMilvus

milvusClient = FaceMilvus(collection_name='face_test1')

# def NewMilvusCLient(table):
#       globla milvusClient
#       milvusClient = FaceMilvus(collection_name=table)


def Store2Milvus(imgID, imgEncoding):
      ids = milvusClient.Insert(imgID, imgEncoding)

def SearchFromMilvus(imgEncoding):
      info = milvusClient.Search(imgEncoding)
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