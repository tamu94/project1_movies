# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
import os
import locale # to format currency as USD
from pandas.io.json import json_normalize
locale.setlocale( locale.LC_ALL, '' )

# Import API key
from api_keys import api_key

# Output File (CSV)
output_data_file = "tmbddata.csv"
## Generate Movies Database from TMBD API by looping though all pages
all_results = []
url = 'https://api.themoviedb.org/3/discover/movie/'
page = 1
while True:
    r = requests.get(url + '?api_key='+ api_key+'&language=en-US' + '&page='+str(page))
    movie_data = r.json()
    if r.status_code == 200:
        all_results.append(movie_data)
        page += 1
    else:
        break

    #Create dataframe - this doesn work!!
df = pd.DataFrame([{
    "release_date":d["release_date"],
    "original_title": d["original_title"],
    "title": d["title"],
    "popularity": d["popularity"],
    "vote_count": d["vote_count"],
    "vote_avg": d["vote_average"],
    "popularity":d["popularity"],
} for d in all_results])

