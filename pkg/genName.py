import time

def GenName():
      # 生成随机名字
      pre = time.time()
      name = str(int(round(pre * 1000)))
      return name