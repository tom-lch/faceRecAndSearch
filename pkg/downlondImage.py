import requests


def DownloadImageByUrl(url, name):
      resp = requests.get(url)
      with open(name, "wb") as f:
            f.write(resp.content)