import pandas as pd
import argparse
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("plot1", help='output of the first scatter plot')
parser.add_argument("plot2", help='output of the second scatter plot')
args = parser.parse_args()

data = pd.read_csv('owid-covid-data-2020-monthly.csv')
#  getting the yearly data only
data = data.groupby(["location"]).agg({"total_cases": "last", "total_deaths": "last"})
data["case_fatality_rate_year"] = data["total_deaths"] / data["total_cases"]

plt.scatter(data['total_cases'], data['case_fatality_rate_year'])
plt.xlabel("Confirmed new cases")
plt.ylabel("Case fatality rate")
plt.title("Scatterplot of case fatality rate vs confirmed cases per country")
plt.savefig(args.plot1)

plt.scatter(data['total_cases'], data['case_fatality_rate_year'])
plt.xscale("log")  #  plot on a log scale
plt.xlabel("Confirmed new cases")
plt.ylabel("Case fatality rate")
plt.title("Scatterplot of case fatality rate vs confirmed cases per country (log scale)")
plt.savefig(args.plot2)
