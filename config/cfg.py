import yaml

Config = read_yaml()

def read_yaml():
      with open('conf.yaml', 'r', encoding='utf-8') as f:
            file_content = f.read()
      conf = yaml.load(file_content, yaml.FullLoader)
      print(conf)

