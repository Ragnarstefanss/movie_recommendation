import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate
import pickle
#sns.set_style("darkgrid")
from surprise import accuracy
from collections import defaultdict
from surprise import KNNBasic
from collections import defaultdict
from operator import itemgetter
import heapq
import os
import csv

# CLEANING UP ORIGINAL KAGGLE FILES
def create_clean_dataframe(number_files=1):
    file_name = 'data/clean_data_'+str(number_files)+'.csv'
    if not os.path.isfile(file_name):
        data = open(file_name, mode='w')
    else:
        return

    if number_files == 1:
        files = ['./data/original/combined_data_1.txt']
    if number_files == 2:
        files = ['./data/original/combined_data_1.txt','./data/original/combined_data_2.txt']
    if number_files == 3:
        files = ['./data/original/combined_data_1.txt','./data/original/combined_data_2.txt', './data/original/combined_data_3.txt']
    if number_files == 4:
        files = ['./data/original/combined_data_1.txt','./data/original/combined_data_2.txt','./data/original/combined_data_3.txt','./data/original/combined_data_4.txt']

    # Remove the line with movie_id: and add a new column of movie_id
    # Combine all data files into a csv file
    for file in files:
        print("Opening file: {}".format(file))
        with open(file) as f:
            for line in f:
                line = line.strip()
                if line.endswith(':'):
                    movie_id = line.replace(':', '')
                else:
                    data.write(movie_id + ',' + line)
                    data.write('\n')
    data.close()

    # Read all data into a pd dataframe
    df = pd.read_csv(file_name, names=['movie_id', 'user_id','rating','date'])
    #print(df.nunique())
    #return df

def first_time_running(max_files=4):
    if max_files < 1: max_files = 1
    if max_files > 4: max_files = 4
    for number in range(1,5):
        if number <= max_files:
            # cleans up number "max_files" of kaggle netflix price data files
            create_clean_dataframe(number)

def get_data(number_of_files_of_rating):
    # if users number_of_files is larger than four or less then 1 then we do not want errors
    if number_of_files_of_rating < 1: number_of_files_of_rating = 1
    if number_of_files_of_rating > 4: number_of_files_of_rating = 4
    file_name_ratings = './data/clean_data_'+str(number_of_files_of_rating)+'.csv'

    movie_titles = pd.read_csv('./data/original/movie_titles.csv', header = None, names = ['movie_id', 'movie_year', 'movie_title'], usecols = [0,1,2], encoding="latin1")
    ratings = pd.read_csv(file_name_ratings, header= None, names = ['movie_id', 'customer_id', 'rating', "date_of_rating"]).drop(['date_of_rating'], axis=1)
    movie_and_rating = ratings.merge(movie_titles, on="movie_id", how="inner")
    return movie_titles, ratings, movie_and_rating
