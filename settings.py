import yaml
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, 'config/db_config.yml')


def get_config(path):
    with open(path) as f:
        config = yaml.load(f)
    return config


config = get_config(config_path)
