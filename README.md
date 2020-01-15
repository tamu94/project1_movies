# API Project - The Movie Buffs 

The goal of this project is to pull data from movie related API's to spot trends regarding movie success. 

We focused on measuring the following data: 
	- box office success compared to release month
	- box office success compared to critic votes 
	- Oscar nominations/wins in regards to release month, critic votes, and box office success. 
	
In an effort to use the most accurate and intuative data, we limited our scope to movies released from 1980 - 2017. 

## Project collaborators

Barry Haygood 
Cathy Egboh 
Maya Saeidi
Michelle Brucato 

## Data Collection 

The API used for this project is TMBD (The Movie Database).

The financial CPI data used for this project was pulled from the FRED website (Federal Reserve Economic Data) as a csv file. 

The Oscars data used for this project was pulled from DataHub.com as a csv file.  There was an option to import the package, "datapackage", however due to installation issues, we had to go the csv route.

## Libraries Used 

Pandas -- to easily import csv files and create data frames 
Matplotlib -- to visualize our data findings using various graphs
Requests -- used to pull data from our API url 
Json_Normalize -- to make the API data more readable 
Blackcellmagic -- to auto format blocks of code for easier readability  
