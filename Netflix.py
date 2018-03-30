#!/usr/bin/env python3
"""NETFLIX ASSIGNMENT
"""
import pickle
import random

# --------
# GLOBALS
# --------

with open("caches/avgCustomerRatings.p", "rb") as f:
    AVG_CUST_CACHE = pickle.load(f)
    f.close()
with open("caches/avgMovieRatings.p", "rb") as f:
    AVG_MOVIE_CACHE = pickle.load(f)
    f.close()
with open("caches/ratingsMovies.p", "rb") as f:
    MOVIE_RATINGS_CACHE = pickle.load(f)
    f.close()
with open("caches/moviePredictionErrorCorrelations.p", "rb") as f:
    MOVIE_PREDICTION_ERROR_CORRELATIONS_CACHE = pickle.load(f)
    f.close()

# I didn't end up using these in the prediction algorithm,
# But for future approaches these could be useful
# with open("caches/yearsSinceRelease.p", "rb") as f:
#     CACHE_YEARS_SINCE_RELEASE = pickle.load(f)
#     f.close()
# with open("caches/movieYears.p", "rb") as f:
#     MOVIE_YEAR_CACHE = pickle.load(f)
#     f.close()


# ------------
# netflix_read
# ------------

def netflix_read(string):
    """
    takes in a line from the input, and determines type of id
    string a string
    return tuple, first value is id, and second is a flag if id is for movies
    """
    val = -1
    ind = -1
    string = string.strip()
    if string.isdigit():
        val = int(string)
        ind = 0
    elif string:
        val = int(string.strip(':'))
        ind = 1
    return (val, ind)

# ------------
# netflix_print
# ------------


def netflix_print(writer, rating):
    """
    prints out to IDs and ratings, rounded to 1 decimal
    writer    a writer
    rating    int (movie id), float(prediction rating),
              or string(RMSE output) to print out
    """
    if isinstance(rating, float):
        writer.write(('%.1f' % rating) + "\n")
    elif isinstance(rating, int):
        writer.write(str(rating) + ":\n")
    else:
        writer.write(rating + "\n")

# ------------
# netflix_solve
# -----------


def netflix_solve(reader, writer):
    """
    takes in the input, outputs predicted ratings, and RMSE
    reader  a reader
    writer  a writer
    """
    movie_id = -1
    actual_rating_list = []
    predict_rating_list = []
    assert len(MOVIE_RATINGS_CACHE.keys()) > 0
    for line in reader:
        u_id, movie_flag = netflix_read(line)
        if movie_flag == 1:
            netflix_print(writer, u_id)
            movie_id = u_id
        else:
            # res = netflix_predict_random(movie_id, u_id)
            # res = netflix_predict_basic(movie_id, u_id)
            res = netflix_predict_with_correlations(movie_id, u_id)
            predict_rating_list.append(res)
            actual_rating_list.append(MOVIE_RATINGS_CACHE[movie_id][u_id])
            netflix_print(writer, res)

    rmse_res = netflix_rmse(actual_rating_list, predict_rating_list)
    netflix_print(writer, "RMSE: " + str(rmse_res))

# ----------------------
# netflix_predict_random
# ----------------------


def netflix_predict_random(movie_id, customer_id):
    """
    movie_id     represents the movie to predict
    customer_id  represents the customer making prediction
    return a float, representing the customer's predicted rating for movie
    """

    # random.random() returns a float [0.0, 1.0)
    res = 1.0 + random.random() * 4

    return res

# ---------------------
# netflix_predict_basic
# ---------------------


def netflix_predict_basic(movie_id, customer_id):
    """
    movie_id     represents the movie to predict
    customer_id  represents the customer making prediction
    return a float, representing the customer's predicted rating for movie
    """

    avg_mov_value = AVG_MOVIE_CACHE[movie_id]
    avg_cust_value = AVG_CUST_CACHE[customer_id]

    res = 3.6736284920068587 + (avg_mov_value - 3.6736284920068587) + (avg_cust_value - 3.6736284920068587)

    # Actual ratings cannot be greater than 5 or less than 1
    if res > 5.0:
        res = 5.0
    elif res < 1.0:
        res = 1.0

    return res

# ---------------------------------
# netflix_predict_with_correlations
# ---------------------------------


def netflix_predict_with_correlations(movie_id, customer_id):
    """
    movie_id     represents the movie to predict
    customer_id  represents the customer making prediction
    return a float, representing the customer's predicted rating for movie
    """

    res = netflix_predict_basic(movie_id, customer_id)

    if movie_id in MOVIE_PREDICTION_ERROR_CORRELATIONS_CACHE:
        for other_movie, corr in MOVIE_PREDICTION_ERROR_CORRELATIONS_CACHE[movie_id].items():

            # If the customer has seen the other movie, use correlation to enhance prediction
            if customer_id in MOVIE_RATINGS_CACHE[other_movie]:
                prediction_error_other_movie = netflix_predict_basic(other_movie, customer_id) - MOVIE_RATINGS_CACHE[other_movie][customer_id]
                res += (corr * prediction_error_other_movie)

    # Actual ratings cannot be greater than 5 or less than 1
    if res > 5.0:
        res = 5.0
    elif res < 1.0:
        res = 1.0

    return res

# ------------
# netflix_rmse
# ------------


def netflix_rmse(answer, pred):
    """
    answer  dictionary or sequence, the answers to compare errors to
    pred    dicitonary or sequence, the predictions made in solve()
    """
    ans = []
    pre = []
    if isinstance(answer, dict) and isinstance(pred, dict):
        for key1, value in pred.items():
            mov = answer[key1]
            for key2, val in value.items():
                pre.append(val)
                ans.append(mov[key2])
        zip_list = zip(ans, pre)
        sum_val = sum([(x - y) ** 2 for x, y in zip_list])
        return (sum_val / len(ans)) ** (0.5)
    else:
        zip_list = zip(answer, pred)
        sum_val = sum([(x - y) ** 2 for x, y in zip_list])
        return (sum_val / len(answer)) ** (0.5)

""" #pragma: no cover
"""
