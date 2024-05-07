import configparser
import os
conf_file_path = os.path.abspath('./hw10_django/utils/conf.ini')


config = configparser.ConfigParser()
config.read('./hw10_django/utils/conf.ini')
print(config.sections())

with open(conf_file_path ,'r') as file:
    x = file.read()
    print(x)