from milvus import Milvus, DataType

class FaceMilvus:
      def __init__(self, host='localhost', port='19530', collection_name='demo_films'):
            self.collection = None
            self.collection_name = collection_name
            self.client = Milvus(host=host, port=port)
            self.collection_param = {
                                    "fields": [
                                          {"name": "imgInfoID", "type": DataType.INT32},
                                          {"name": "imgEncoding", "type": DataType.FLOAT_VECTOR, "params": {"dim": 128}}
                                    ],
                                    "segment_row_limit": 100000,
                                    "auto_id": True
                                    }
            self.collection = self.collection if self.collection  else self._create_collection()
      def _create_collection(self):
            if self.collection_name in self.client.list_collections() :
                  return 
            return self.client.create_collection(self.collection_name, self.collection_param)

      def _delete_collection(self, collection_name):
            self.client.drop_collection(collection_name)
      
      def Delete(self, collection_name):
            self._delete_collection(collection_name)

      def Insert(self, imgInfoID, imgEncoding):
            hybrid_entities = [
                                    # {"name": "duration", "values": list_of_int, "type": DataType.INT32},
                                    # {"name": "release_year", "values": list_of_int, "type": DataType.INT64},
                                    # {"name": "embedding", "values": vectors, "type":DataType.FLOAT_VECTOR},
                                    {"name": "imgInfoID", "values": [imgInfoID], "type": DataType.INT32},
                                    {"name": "imgEncoding", "values": [imgEncoding],"type": DataType.FLOAT_VECTOR}
                              ]
            ids = self.client.insert(self.collection_name, hybrid_entities)
            self.Flush()
            return ids
      
      def DeleteByIds(self, ids):
            # ids = [1,]
            self.client.delete_entity_by_id(self.collection_name, ids) 
            self.Flush()

      def CreateIndex(self, index_type='IVF_FLAT', metric_type='L2', params={"dim": 4096}):
            ivf_param = {"index_type": index_type, "metric_type": metric_type, "params": params}
            self.client.create_index(self.collection_name, "Vec", ivf_param)
      
      def DropIndex(self, index_name):
            self.client.drop_index(self.collection_name, index_name)


      def Search(self, imgEncoding, partition_tags=None, fields=None, timeout=None):
            # dsl = {
            #             "bool": {
            #                   "must":[
            #                         {
            #                         "term": {"A": [1, 2, 5]}
            #                         },
            #                         {
            #                         "range": {"B": {"GT": 1, "LT": 100}}
            #                         },
            #                         {
            #                         "vector": {
            #                               "Vec": {"topk": 10, "query": vectors[:1], "metric_type": "L2", "params": {"nprobe": 10}}
            #                         }
            #                         }
            #                   ]
            #             }
            #       }
            query_hybrid = {
                  "bool": {
                        "must": [
                              {
                              "vector": {
                                    "imgEncoding": {"topk": 3, "query": [imgEncoding], "metric_type": "L2"}
                              }
                              }
                        ]
                  }
            }

            entities_list = self.client.search(self.collection_name, query_hybrid, fields=["imgInfoID"])
            results = []
            for entities in entities_list:
                  for topk_film in entities:
                        result = {}
                        current_entity = topk_film.entity
                        print("- id: {}".format(topk_film.id))
                        print("- distance: {}".format(topk_film.distance))
                        print("- imgInfoID: {}".format(current_entity.imgInfoID))
                        result["id"] = topk_film.id
                        result["distance"] = topk_film.distance
                        result["imgInfoID"] = current_entity.imgInfoID
                        results.append(result)
            return results

      def Flush(self):
            self.client.flush([self.collection_name])

      def GetStatus(self):
            info = self.client.get_collection_stats(self.collection_name)
            return info
