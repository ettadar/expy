import os
import json
import hashlib
from copy import deepcopy
from expy.experiment_pool import set_param_value, get_param_value, generate_exp_hash

def is_int(value):
  try:
    int(value)
    return True
  except ValueError:
    return False

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

def add_param(results_directory, param, value, param_test=None, value_test=None):
    for exp_dir in os.listdir(results_directory):
        print os.path.join(results_directory, exp_dir)

        if not os.path.isfile(os.path.join(results_directory, exp_dir, "0", "params.json")):
            print "No param file found : ", exp_dir
            continue

        with open(os.path.join(results_directory, exp_dir, "0", "params.json"), "r") as old_params_file:
            old_params = json.load(old_params_file)

        if param_test is not None and (get_param_value(old_params, param_test) != value_test):
            continue

        new_params = deepcopy(old_params)
        set_param_value(new_params, param, value)

        print " ->", os.path.join(results_directory, generate_exp_hash(new_params))

        for exp_unit_dir in os.listdir(os.path.join(results_directory, exp_dir)):
            if os.path.isdir(os.path.join(results_directory, exp_dir, exp_unit_dir)):
                assert exp_unit_dir.isdigit()
                with open(os.path.join(results_directory, exp_dir, exp_unit_dir, "params.json"), "r") as old_params_file:
                    assert old_params == json.load(old_params_file)
                with open(os.path.join(results_directory, exp_dir, exp_unit_dir, "params.json"), "w") as new_params_file:
                    json.dump(new_params, new_params_file)

        os.rename(os.path.join(results_directory, exp_dir),
            os.path.join(results_directory, generate_exp_hash(new_params)))


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 4:
        value = sys.argv[3]
        if is_int(value):
            value = int(value)
        elif is_float(value):
            value = float(value)
        elif str_to_bool(value) is not None:
            value = str_to_bool(value)
        add_param(sys.argv[1], sys.argv[2], value)

    elif len(sys.argv) == 6:
        value = sys.argv[3]
        if is_int(value):
            value = int(value)
        elif is_float(value):
            value = float(value)
        elif str_to_bool(value) is not None:
            value = str_to_bool(value)

        value_test = sys.argv[5]
        if is_float(value_test):
            value_test = float(value_test)
        elif str_to_bool(value) is not None:
            value_test = str_to_bool(value_test)

        add_param(sys.argv[1], sys.argv[2], value, sys.argv[4], value_test)
    else:
        print "Usage : python {} <results_directory> <param> <value> [<param_test> <value_test>]".format(sys.argv[0])