import numpy as np
import pandas as pd
import random

df = '../Basic-Analysis/Dataset/Censo Forestal.csv'
df = pd.read_csv(df)
"""
count = {}
for c in df['NOMBRE_CIENTIFICO']:
    c=c.strip()
    if c in count:
        count[c] += 1
    else:
        count[c] = 1
"""
#print(count)
#print("Minimum Coutned :",np.min(list(count.values())))

def find_random_per_species(df):
    selected_list = []
    class_names = df['NOMBRE_CIENTIFICO'].unique()
    #sel = random.choices(class_name, k=10)
    for cls in class_names:
        cls_rows = df[df['NOMBRE_CIENTIFICO'] == cls]
        k = min(5, len(cls_rows))

        sampled_row = cls_rows.sample(n=k, random_state=42)

        selected_list.append(sampled_row)
    sel=pd.concat(selected_list)

    print(sel)
    sel.to_csv('output.csv')
    return(sel)
    """for label in df['NOMBRE_CIENTIFICO']:
        print
        print(sel)"""

find_random_per_species(df)