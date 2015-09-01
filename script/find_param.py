import os
import json
from expy.experiment_pool import get_param_value, generate_exp_hash
import shutil

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def str_to_bool(value):
    if value in ["True", "true"]:
        return True
    if value in ["False", "false"]:
        return False
    return None

def find_param(results_directory, param, value):
    for exp_dir in os.listdir(results_directory):
        with open(os.path.join(results_directory, exp_dir, "0", "params.json"), "r") as params_file:
            params = json.load(params_file)
        
        try:
            if get_param_value(params, param) == value:
                print os.path.join(results_directory, exp_dir)
                # To remove the directories:
                # shutil.rmtree(os.path.join(results_directory, exp_dir))
        except:
            pass

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 4:
        value = sys.argv[3]
        if is_float(value):
            value = float(value)
        elif str_to_bool(value) is not None:
            value = str_to_bool(value)
        find_param(sys.argv[1], sys.argv[2], value)
    else:
        print "Usage : python {} <results_directory> <param> <value>".format(sys.argv[0])
