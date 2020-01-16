# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
import os
import locale  # to format currency as USD
from pandas.io.json import json_normalize
import datetime

locale.setlocale(locale.LC_ALL, "")

# Import API key
from api_keys import api_key

# Output File (CSV)
output_data_file = "tmbddata_dev.csv"
movie_revenue_data = "tmbd_dev_movie_revenue.csv"
final_data = "tmbd_data_final.csv"

## Generate Movies Database from TMBD API by looping though all pages
all_results = []
url = "https://api.themoviedb.org/3/discover/movie/"
page = 1
while True:
    r = requests.get(
        url + "?api_key=" + api_key + "&language=en-US" + "&page=" + str(page)
    )
    movie_data = r.json()
    if r.status_code == 200:
        all_results.append(movie_data)
        page += 1
    else:
        break
# Create dataframe to store movie data movie_df
movie_df = pd.io.json.json_normalize(all_results, record_path="results")
# create CSV file of raw data from OpenWeather API and store in Results Directory
# Create directory to store results
script_dir = os.path.dirname("")
results_dir = os.path.join(script_dir, "Results/")
if not os.path.isdir(results_dir):
    os.makedirs(results_dir)
movie_df.to_csv(results_dir + output_data_file)
# Create list of movie ids from dataframe to use in APU query and get revenue and budget
movie_ids = movie_df["id"].tolist()
# Create function to query database by movie id and get detailed data
def get_movie_revenue(id, api_key):

    url = "https://api.themoviedb.org/3/movie/"

    r = requests.get(
        url
        + str(id)
        + "?api_key="
        + api_key
        + "&language=en-US"
        + "&sort_by=revenue.desc"
    )

    if r.status_code == 200:
        return r.json()
    else:
        return None

movie_revenue = []

for id in movie_ids:
    result = get_movie_revenue(id, api_key)
    if result:
        movie_revenue.append(result)

# Create movie_revenue_df and Save data to csv file
movie_revenue_df = pd.io.json.json_normalize(movie_revenue)
movie_revenue_df.to_csv(results_dir + movie_revenue_data)

# Import FRED Consumer Price Index for Urban Consumers https://fred.stlouisfed.org/series/CPIAUCNS

path = os.path.join("Data", "CPIAUCNS.csv")
inflation_df = pd.read_csv(path)

# Clean Data for movie_revenue_df
# Get names of indexes for which revenue column has revenue has value of less than or equal to zero
# Delete these rows from dataframe

indexNames = movie_revenue_df[movie_revenue_df["revenue"] <= 0].index
movie_revenue_df.drop(indexNames, inplace=True)

# Get names of indexes for which budget column has revenue has value of less than or equal to zero
# Delete these rows from dataframe

indexNames = movie_revenue_df[movie_revenue_df["budget"] <= 0].index
movie_revenue_df.drop(indexNames, inplace=True)

# Add column "Profit" which is revenue - budget

movie_revenue_df["profit"] = movie_revenue_df["revenue"] - movie_revenue_df["budget"]

# Convert release date to month/year and create new column called release month

movie_revenue_df["month"] = pd.to_datetime(
    movie_revenue_df["release_date"]
).dt.to_period("M")

# Remove columns we dont need and create new dataframe movie_revenue_clean_df

columns_drop = [
    "adult",
    "backdrop_path",
    "belongs_to_collection",
    "poster_path",
    "genres",
    "tagline",
    "video",
    "belongs_to_collection.id",
    "belongs_to_collection.name",
    "belongs_to_collection.poster_path",
    "belongs_to_collection.backdrop_path",
]
movie_revenue_df.drop(columns_drop, axis=1, inplace=True)

# create index multiplier
inflation_df["CPI_multiplier"] = (
    inflation_df["CPIAUCNS"].iloc[-1] / inflation_df["CPIAUCNS"]
)

# Convert release date to month/year and create new column called release month
inflation_df["month"] = pd.to_datetime(inflation_df["DATE"]).dt.to_period("M")

# Merge CPI dataframe to movie_revenue_df by matching month

final_df = pd.merge(movie_revenue_df, inflation_df, how="left", on="month")

# Create CPI adjusted profit revenue and budget columns
final_df["CPIAdjProfit"] = final_df["profit"] * final_df["CPI_multiplier"]
final_df["CPIAdjRevenue"] = final_df["revenue"] * final_df["CPI_multiplier"]
final_df["CPIAdjBudget"] = final_df["budget"] * final_df["CPI_multiplier"]

# Remove new releases from dataset (released after 11/1/19)
indexNames = final_df[final_df["month"] > datetime.date(2019, 11, 1)].index
final_df.drop(indexNames, inplace=True)

# Save final data to csv file

final_df.to_csv(results_dir + final_data)

# Create new dataframe with pre 1980 Release Data removed
tmbd_data_post_1980_df = final_df
tmbd_data_post_1980_df = tmbd_data_post_1980_df
indexNames = tmbd_data_post_1980_df[tmbd_data_post_1980_df["month"] < datetime.date(1980, 1, 1)].index
tmbd_data_post_1980_df.drop(indexNames, inplace=True)

# Save tmbd_data_post_1980 to csv file

tmbd_data_post_1980_df.to_csv(results_dir + "TMBD_data_post_1980.csv")

#Load oscar data to dataframe
path = os.path.join("Data", "data_csv.csv")
oscars_df = pd.read_csv(path)

#Merge Oscar data with post 1980 movie data to create best picture (bestpic_post_1980_df)
bestpic_df = pd.merge(tmbd_data_post_1980_df, oscars_df, how = "left", left_on ="title", right_on='entity')

#Create conditions to annote Best_Picture Winner,Nominee, No

cond1 = bestpic_df.category.str.contains('BEST PICTURE')
cond2 = bestpic_df.winner = True
bestpic_df['category'] = bestpic_df['category'].fillna('missing')

bestpic_df['Best_Picture'] = np.where(np.logical_and(cond1 == True, cond2), "Winner", "Nominee")

bestpic_df.loc[bestpic_df['category'].str.contains("BEST PICTURE")==0,'Best_Picture'] = "No"

# Save bestpic_df to csv file
bestpic_df.to_csv(results_dir + "TMBD_Data_best_picture.csv")