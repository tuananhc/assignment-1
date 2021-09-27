import pandas as pd
import argparse 
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()

#  function to sum values across a groupby item that disregard NaN values unless all values are NaN 
def sumNaN(group): 
    if np.isnan(group).all():
        return np.NaN
    else:
        return group.sum(skipna=True)

data = pd.read_csv("owid-covid-data.csv")

#  change date formate
data['date'] = pd.to_datetime(data['date'])

#  create column month to group later
data['month'] = data['date'].dt.month 

#  getting values from year 2020 only
output = data[data['date'].dt.year == 2020]
output = output.groupby([output['location'], output['month']]).agg({'total_cases': 'last', 'new_cases': sumNaN, 'total_deaths': 'last', 'new_deaths': sumNaN})
output["case_fatality_rate"] = output["new_deaths"] / output["new_cases"]
output = output[["case_fatality_rate", "total_cases", "new_cases", "total_deaths", "new_deaths"]]

print(output.head());
output.to_csv(args.filename);
