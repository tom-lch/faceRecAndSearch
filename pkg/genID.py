import uuid
import time
import random

def _genUUID():
      return str(uuid.uuid4())

def GenID():
      # return _genUUID
      return _genIDByTime()

def _genIDByTime():
      return  int(time.time() * 1000)  * 1000 + random.randint(0, 1000)