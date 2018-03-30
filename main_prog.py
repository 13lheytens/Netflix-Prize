#!/usr/bin/env python3

# -------
# imports
# -------

import pickle
import sys

from Netflix import netflix_solve

# ----
# main
# ----

with open("caches/moviePredictionErrorCorrelations.p", "rb") as f:
    CORRELATIONS = pickle.load(f)
    f.close()

with open("caches/ratingsCustomers.p", "rb") as f:
    MOVIE_RATINGS_CACHE = pickle.load(f)
    f.close()

for movie_id, cust_obj in CORRELATIONS.items():
	print(str(movie_id) + ": " + str(cust_obj))

total_avg = 0
total_num = 0
for movie_id, cust_dict in MOVIE_RATINGS_CACHE.items():
	for cust_id, rating in cust_dict.items():
		total_avg += rating
		total_num += 1

print (str(total_avg / total_num))


""" #pragma: no cover
"""
