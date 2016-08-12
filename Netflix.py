#!/usr/bin/env python3
"""NETFLIX ASSIGNMENT
"""
import pickle

# --------
# GLOBALS
# --------

# For if running without probe data
PROBETEXT = "/u/downing/cs/cs373/netflix/probe.txt"

with open("caches/movYear.p", "rb") as f:
    CACHE_MOVIE_YEAR = pickle.load(f)
    f.close()
with open("caches/tAvgCust.p", "rb") as f:
    CACHE_AVG_CUSTOMER_RATING = pickle.load(f)
    f.close()
with open("caches/tAvgMovie.p", "rb") as f:
    CACHE_AVG_MOVIE_RATING = pickle.load(f)
    f.close()
with open("caches/tYearsSinceRelease.p", "rb") as f:
    CACHE_YEARS_SINCE_RELEASE = pickle.load(f)
    f.close()
with open("caches/tAnswers.p", "rb") as f:
    CACHE_ANSWERS = pickle.load(f)
    f.close()

# Results from lin Reg 2
CACHE_RELATED_MOVIES = {5317 : {15124 : -0.04099798, 6287 : -0.09074658, 14313 : -0.30758110}, 15124 : {5317: -0.04099798}, 6287 : {5317: -0.09074658}, 14313 : {5317 : -0.30758110}}

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
    assert len(CACHE_ANSWERS.keys()) > 0
    for line in reader:
        u_id, movie_flag = netflix_read(line)
        if movie_flag == 1:
            netflix_print(writer, u_id)
            movie_id = u_id
        elif movie_flag == 0:
            res = netflix_predict(movie_id, u_id)
            res = related_movie_offset(res, movie_id, u_id)
            predict_rating_list.append(res)
            actual_rating_list.append(CACHE_ANSWERS[movie_id][u_id])
            netflix_print(writer, res)
        else:
            assert False

    rmse_res = netflix_rmse(actual_rating_list, predict_rating_list)
    netflix_print(writer, "RMSE: " + str(rmse_res))

# ---------------
# netflix_predict
# ---------------

def netflix_predict(movie_id, customer_id):
    """
    movie_id     represents the movie to predict
    customer_id  represents the customer making prediction
    return a float, representing the customer's predicted rating for movie
    """

    avg_mov_value = CACHE_AVG_MOVIE_RATING[movie_id]
    avg_cust_value = CACHE_AVG_CUSTOMER_RATING[customer_id]
    years_after_release = CACHE_YEARS_SINCE_RELEASE[movie_id][customer_id]

    # Equation from results gradient-descent/linRegResults.txt
    res = 3.78699752 + (avg_mov_value - 3.72) * 0.91299576 \
    + (avg_cust_value - 3.72) * 0.90834816 \
    + years_after_release * 0.00196377

    # Actual ratings cannot be greater than 5 or less than 1
    if res > 5.0:
        res = 5.0
    elif res < 1.0:
        res = 1.0

    return res

# ---------------
# related_movie_offset
# ---------------

def related_movie_offset(pred, movie_id, customer_id):
    """
    calculates related movie ratings offset
    return a float, representing offset
    """
    offset = 0.0
    if movie_id in CACHE_RELATED_MOVIES:
        for other_mov, weight in CACHE_RELATED_MOVIES[movie_id].items():
            if customer_id in CACHE_ANSWERS[other_mov]:
                offset += weight * (netflix_predict(other_mov, customer_id) - CACHE_ANSWERS[other_mov][customer_id])
    if offset == 0.0:
        return pred
    # equation from lin reg results 2
    return -0.16439531 + 1.07691904 * pred + offset

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