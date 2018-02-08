import os
from config import config_saving


def make_dirs(data, model_name):
    path = os.path.join(config_saving['dir_name'], model_name, data)
    if not os.path.exists(path):
        os.makedirs(path)
    return path
