import yaml


def getConfig():
    with open("config.yaml", 'r') as configFile:
        try:
            return yaml.safe_load(configFile)
        except yaml.YAMLError as e:
            print(e)