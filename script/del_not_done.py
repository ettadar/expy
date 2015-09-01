import os
import json
from expy.experiment_pool import get_param_value, generate_exp_hash
import shutil

def find_param(results_directory):
    for exp_dir in os.listdir(results_directory):
        for exp_unit_dir in os.listdir(os.path.join(results_directory, exp_dir)):
            if os.path.isdir(os.path.join(results_directory, exp_dir, exp_unit_dir)):
                trial_dir = os.path.join(results_directory, exp_dir, exp_unit_dir)
                if not os.path.isfile(os.path.join(trial_dir, "results.json")):
                    shutil.rmtree(trial_dir)

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        find_param(sys.argv[1])
    else:
        print "Usage : python {} <results_directory>".format(sys.argv[0])
