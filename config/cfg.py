import yaml

def read_yaml(file):
      with open(file, 'r', encoding='utf-8') as f:
            file_content = f.read()
      conf = yaml.load(file_content, yaml.FullLoader)
      print(conf)
      return conf

Config = read_yaml('./conf.yaml')



