#!/usr/bin/env python3

import sys
import pickle
import os
import numpy

# --------
# GLOBALS
# --------

# Directory of Data files
NETFLIX_DATA_FILES_DIR = "../data/"

# Movie Base Caches
MOVIE_RATINGS_CACHE = {}
AVG_MOVIE_CACHE = {}
MOVIE_YEAR_CACHE = {}
YEARS_PASSED_SINCE_RELEASE_CACHE = {}
MOVIE_PREDICTION_ERROR_CORRELATIONS_CACHE = {}

# Customer Based Caches
CUSTOMER_RATINGS_CACHE = {}
AVG_CUST_CACHE = {}

# For Debugging
PRINT_OUTPUT = 1

def create_caches_from_training_data():

    # I moved the training data files into its own folder "trainingSet"
    base_dir = NETFLIX_DATA_FILES_DIR + "training_set"
    count_movies = 0
    for subdir, dirs, files in os.walk(base_dir):
        for cur_file in files:
            opened_file = open(base_dir + "/" + cur_file,
                               "r", encoding='latin-1')
            movie_id = -1
            for line in opened_file:
                line = line.strip()

                # Movie ID is represented as "movie_id:"
                if ':' in line:
                    count_movies += 1
                    if PRINT_OUTPUT:
                        print("Movie Number: " + str(count_movies))
                    line = line[:-1]
                    movie_id = int(line)

                    # Initialize Movie Based Caches for this movie
                    MOVIE_RATINGS_CACHE[movie_id] = {}
                    YEARS_PASSED_SINCE_RELEASE_CACHE[movie_id] = {}
                    AVG_MOVIE_CACHE[movie_id] = 0

                # Every other line is "cust_id,rating,rating_date"
                # "rating_date" is formatted as YYYY-MM-DD
                else:
                    line_info = line.split(',')
                    cust_id = int(line_info[0])
                    rating = int(line_info[1])
                    rating_date = line_info[2]

                    # Check if customer already exists in the caches
                    # If not, initialize Customer Based Caches for this customer
                    if cust_id not in CUSTOMER_RATINGS_CACHE:
                        CUSTOMER_RATINGS_CACHE[cust_id] = {}
                        AVG_CUST_CACHE[cust_id] = 0

                    # Update Ratings Caches
                    MOVIE_RATINGS_CACHE[movie_id][cust_id] = rating
                    CUSTOMER_RATINGS_CACHE[cust_id][movie_id] = rating

                    # Update Average Customer Rating Cache and Average Movie Rating Cache
                    # Currently summing (instead of finding average)
                    # Averages will be found on a second iteration below
                    AVG_MOVIE_CACHE[movie_id] += rating
                    AVG_CUST_CACHE[cust_id] += rating

                    # Update Years Passed Since Release Cache
                    # Note the use of MOVIE_YEAR_CACHE. This must be created
                    # beforehand
                    year_watched = int(rating_date.split('-')[0])
                    YEARS_PASSED_SINCE_RELEASE_CACHE[movie_id][
                        cust_id] = year_watched - MOVIE_YEAR_CACHE[movie_id]
            opened_file.close()

        # Iterate through again to turn sums into averages
        for movie_id, cust_dict in MOVIE_RATINGS_CACHE.items():
            AVG_MOVIE_CACHE[movie_id] /= len(cust_dict)

        for cust_id, movie_dict in CUSTOMER_RATINGS_CACHE.items():
            AVG_CUST_CACHE[cust_id] /= len(movie_dict)


def create_caches_from_movie_data():
    mov_file = open(NETFLIX_DATA_FILES_DIR +
                    "movie_titles.csv", "r", encoding='latin-1')
    for line in mov_file:
        line = line.strip()

        # line is now "movie_id,movie_year,movie_title"
        line_info = line.split(",")
        movie_id = int(line_info[0])
        try:
            MOVIE_YEAR_CACHE[movie_id] = int(line_info[1])
        except:
            # If "year" is Null, too old
            MOVIE_YEAR_CACHE[movie_id] = 1900


def get_top_three_occurring_movies():

    # Top 3 with be [first, second, third]
    top_3 = [-1, -1, -1]
    for key, value_dict in MOVIE_RATINGS_CACHE.items():
        if len(value_dict) > top_3[0]:
            top_3[2] = top_3[1]
            top_3[1] = top_3[0]
            top_3[0] = key
        elif len(value_dict) > top_3[1]:
            top_3[2] = top_3[1]
            top_3[1] = key
        elif len(value_dict) > top_3[2]:
            top_3[2] = key

    return top_3

# Basic Prediction Algorithm Error
def get_basic_prediction_error(movie_id, cust_id):

    # Simpler Prediction Algorithm
    avg_mov_value = AVG_MOVIE_CACHE[movie_id]
    avg_cust_value = AVG_CUST_CACHE[cust_id]

    prediction = 3.6736284920068587 + (avg_mov_value - 3.6736284920068587) + (avg_cust_value - 3.6736284920068587)

    # Actual ratings cannot be greater than 5 or less than 1
    if prediction > 5.0:
        prediction = 5.0
    elif prediction < 1.0:
        prediction = 1.0

    answer = MOVIE_RATINGS_CACHE[movie_id][cust_id]
    return prediction - answer

# This function finds how correlated the prediction errors are between Movies (using the prediction approach above)
# Example: If customer A rates Movie1 above what was predicted, 
#          and he also rates Movie2 above what was predicted,
#          this demonstrates a positive correlation between Movie1 and Movie2
def create_movie_prediction_error_correlations_cache():

    # Get Top 3 watched movies
    top_3_watched = get_top_three_occurring_movies()
    first = top_3_watched[0]
    second = top_3_watched[1]
    third = top_3_watched[2]

    # Prediction Errors Info that will be used to calculate correlations between movies
    first_second_prediction_errors = {first: [], second: []}
    first_third_prediction_errors = {first: [], third: []}
    second_third_prediction_errors = {second: [], third: []}

    for cust_id, movie_dict in CUSTOMER_RATINGS_CACHE.items():
        movies_watched = set(movie_dict.keys())
        if first in movies_watched and second in movies_watched:
            first_second_prediction_errors[first].append(get_basic_prediction_error(first, cust_id))
            first_second_prediction_errors[second].append(get_basic_prediction_error(second, cust_id))
        if first in movies_watched and third in movies_watched:
            first_third_prediction_errors[first].append(get_basic_prediction_error(first, cust_id))
            first_third_prediction_errors[third].append(get_basic_prediction_error(third, cust_id))
        if second in movies_watched and third in movies_watched:
            second_third_prediction_errors[second].append(get_basic_prediction_error(second, cust_id))
            second_third_prediction_errors[third].append(get_basic_prediction_error(third, cust_id))

    if PRINT_OUTPUT:
        # Enhancement: Use real names instead of Movie1, Movie2, and Movie3
        print("Number of Customers that seen both Movie1 and Movie2: " + str(len(first_second_prediction_errors[first])))
        print("Number of Customers that seen both Movie1 and Movie3: " + str(len(first_third_prediction_errors[first])))
        print("Number of Customers that seen both Movie2 and Movie3: " + str(len(second_third_prediction_errors[second])))

    first_second_correlation = numpy.corrcoef(first_second_prediction_errors[first], first_second_prediction_errors[second])[0, 1]
    first_third_correlation = numpy.corrcoef(first_third_prediction_errors[first], first_third_prediction_errors[third])[0, 1]
    second_third_correlation = numpy.corrcoef(second_third_prediction_errors[second], second_third_prediction_errors[third])[0, 1]

    MOVIE_PREDICTION_ERROR_CORRELATIONS_CACHE[first] = {second: first_second_correlation, third: first_third_correlation}
    MOVIE_PREDICTION_ERROR_CORRELATIONS_CACHE[second] = {first: first_second_correlation, third: second_third_correlation}
    MOVIE_PREDICTION_ERROR_CORRELATIONS_CACHE[third] = {first: first_third_correlation, second: second_third_correlation}

if __name__ == "__main__":

    # Create the Caches
    create_caches_from_movie_data()
    if PRINT_OUTPUT:
        print("Finished creating caches from Movie Data")

    create_caches_from_training_data()
    if PRINT_OUTPUT:
        print("Finished creating caches from Training Data")

    create_movie_prediction_error_correlations_cache()
    if PRINT_OUTPUT:
        print("Finished creating Movie Prediction Error Correlation Caches")

    # Create Pickle Files
    with open("movieYears.p", "wb") as f:
        pickle.dump(MOVIE_YEAR_CACHE, f)
        f.close()
    if PRINT_OUTPUT:
        print("Finished creating Movie Year Pickle file")

    with open("ratingsMovies.p", "wb") as f:
        pickle.dump(MOVIE_RATINGS_CACHE, f)
        f.close()
    if PRINT_OUTPUT:
        print("Finished creating Movie Ratings Pickle file")

    with open("ratingsCustomers.p", "wb") as f:
        pickle.dump(CUSTOMER_RATINGS_CACHE, f)
        f.close()
    if PRINT_OUTPUT:
        print("Finished creating Customer Ratings Pickle file")

    with open("yearsSinceRelease.p", "wb") as f:
        pickle.dump(YEARS_PASSED_SINCE_RELEASE_CACHE, f)
        f.close()
    if PRINT_OUTPUT:
        print("Finished creating Years Since Release Pickle file")

    with open("avgMovieRatings.p", "wb") as f:
        pickle.dump(AVG_MOVIE_CACHE, f)
        f.close()
    if PRINT_OUTPUT:
        print("Finished creating Average Movie Ratings Pickle file")

    with open("avgCustomerRatings.p", "wb") as f:
        pickle.dump(CUSTOMER_RATINGS_CACHE, f)
        f.close()
    if PRINT_OUTPUT:
        print("Finished creating Average Customer Ratings Pickle file")

    with open("moviePredictionErrorCorrelations.p", "wb") as f:
        pickle.dump(MOVIE_PREDICTION_ERROR_CORRELATIONS_CACHE, f)
        f.close()
    if PRINT_OUTPUT:
        print("Finished creating Movie Prediction Error Correlations Pickle file")
