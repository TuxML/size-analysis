from load_dataset import load_dataset
from params import get_params, get_possible_configurations

import traceback

import tux


params, hyperparams_list = get_params()

configs = get_possible_configurations(hyperparams_list)

print(params)
print(hyperparams_list)

df = load_dataset(params["nb_yes"])
params["dataset"] = df

if len(configs) > 0:
    for config in configs:
        
        for k,v in config.items():
            params["hyperparams"][k] = v
        
        try:
            ml = tux.TuxML(**params)
        except Exception as e:
            print(traceback.format_exc())
            print(e)
        print("Starting")

        try:
            ml.start()
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            print("Fails")
else:
    
        try:
             ml = tux.TuxML(**params)
        except Exception as e:
            print(traceback.format_exc())
            print(e)
        print("Starting")

        try:
            ml.start()
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            print("Fails")
print("End")