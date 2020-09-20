import os
import pandas as pd
import json

print(os.getcwd())
os.chdir('../..')
print(os.getcwd())

dfx = pd.DataFrame(json.load(open("finsmes.json")))
print(dfx)