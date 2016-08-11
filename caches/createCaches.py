#!/usr/bin/env python3

import pickle
import sys
import os

# --------
# GLOBALS
# --------

ANS_CACHE = {}
YEARS_PASSED_SINCE_RELEASE_CACHE = {}
MOV_YEAR_CACHE = {}
AVG_CUST_CACHE = {}
AVG_MOVIE_CACHE = {}

def createAnswerYearCaches():
    BASE = "/u/downing/cs/netflix/training_set"
    count_movies = 0;
    for subdir, dirs, files in os.walk(BASE):
        for fil in files:
            count_movies += 1
            f = open(BASE + "/" + fil, "rb")
            firstLine = True
            movie_id = -1
            cust_rat_dict = {}
            cust_years_passed_dict = {}
            for line in f:
                lineStr = str(line)[2:]
                # First Line of each file is "movie_id:"
                if firstLine:
                    line_info = lineStr.split(':')
                    print("Movie Number: " + str(count_movies))
                    movie_id = int(line_info[0])
                    firstLine = False
                # Every other line is "cust_id,cust_rating,rating_date"
                # "rating_date" is formatted as YYYY-MM-DD
                else:
                    line_info = lineStr.split(',')
                    cust_id = int(line_info[0])
                    cust_rat_dict[cust_id] = int(line_info[1])
                    x = line_info[2].split('-')
                    cust_years_passed_dict[cust_id] = int(x[0]) - MOV_YEAR_CACHE[movie_id]
            ANS_CACHE[movie_id] = cust_rat_dict
            YEARS_PASSED_SINCE_RELEASE_CACHE[movie_id] = cust_years_passed_dict


def createMovieYearCache():
    mov_file = open("/u/downing/cs/netflix/movie_titles.txt", "rb")
    for line in mov_file:
        lineStr = str(line)[2:]
        # lineStr is now "movie_id,movie_year,movie_title"
        lineInfo = lineStr.split(",")
        mov_id = int(lineInfo[0])
        try:
            MOV_YEAR_CACHE[mov_id] = int(lineInfo[1])
        except:
            # When "year" is Null
            MOV_YEAR_CACHE[mov_id] = 1900

def createAvgMovieCache(ans):
    for movie_id, cust_dict in ans.items():
        sum = 0
        count = 0.0
        for cust_id, cust_rat in cust_dict.items():
            sum += cust_rat
            count += 1.0
        AVG_MOVIE_CACHE[movie_id] = sum / count

def createAvgCustCache(ans):
    # Keeps track of sum and count of ratings
    TEMP_CUST_CACHE = {}
    for movie_id, cust_dict in ans.items():
        for cust_id, cust_rat in cust_dict.items():
            if cust_id in TEMP_CUST_CACHE:
                TEMP_CUST_CACHE[cust_id][0] += cust_rat
                TEMP_CUST_CACHE[cust_id][1] += 1.0
            else:
                sum_count_arr = [cust_rat, 1.0]
                TEMP_CUST_CACHE[k] = sum_count_arr
    for movie_id, cust_arr in TEMP_CUST_CACHE.items():
        AVG_CUST_CACHE[movie_id] = cust_arr[0] / cust_arr[1]


if __name__ == "__main__":
    createMovieYearCache()
    print("Finished Creating Movie Year Cache")
    with open("movYear.p", "wb") as f:
        pickle.dump(MOV_YEAR_CACHE, f)
        f.close()
    print("Finished creating Pickle of Movie Year Cache")
    createAnswerYearCaches()
    print("Finished Creating Answer Cache and Years Passed Since Release Cache")
    with open("tAnswers.p", "wb") as f:
        pickle.dump(ANS_CACHE, f)
        f.close()
    print("Finished creating Pickle of Answer Cache")
    with open("tYearsSinceRelease.p", "wb") as f:
        pickle.dump(YEARS_PASSED_SINCE_RELEASE_CACHE, f)
        f.close()
    print("Finished creating Pickle of Years Passed Since Release Cache")
    createAvgMovieCache(ANS_CACHE)
    print("Finished Creating Average Movie Cache")
    with open("tAvgMovie.p", "wb") as f:
        pickle.dump(AVG_MOVIE_CACHE, f)
        f.close()
    print("Finished creating Pickle of Average Movie Cache")
    createAvgCustCache(ANS_CACHE)
    print("Finished creating Average Customer Cache")
    with open("tAvgCust.p", "wb") as f:
        pickle.dump(AVG_CUST_CACHE, f)
        f.close()
    print("Finished creating Pickle of Average Customer Cache")