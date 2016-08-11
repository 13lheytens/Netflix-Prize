#!/usr/bin/env python3

import pickle
from urllib.request import urlopen

# --------
# GLOBALS
# --------

with open("caches/tAvgCust.p", "rb") as f:
	CACHE_AVG_CUSTOMER_RATING = pickle.load(f)
	f.close()
with open("caches/tAvgMovie.p", "rb") as f:
	CACHE_AVG_MOVIE_RATING = pickle.load(f)
	f.close()
#CACHE_FAV_MOVIE_YEARS = pickle.load(open("caches/custFavYears2.p", "rb"))
#CACHE_LEAST_FAV_MOVIE_YEARS = pickle.load(open("caches/custLeastFavYears2.p", "rb"))
with open("caches/movYear.p", "rb") as f:
	CACHE_MOVIE_YEAR = pickle.load(f)
	f.close()
with open("caches/tAnswers.p", "rb") as f:
	ANSWERS_CACHE = pickle.load(f)
	f.close()
with open("caches/tYearsSinceRelease.p", "rb") as f:
	YEARS_AFTER_RELEASE = pickle.load(f)
	f.close()


def createFile():
	avg = 3.72
	for mov_id, cust_arr in ANSWERS_CACHE.items():
		for cust_id, rat in cust_arr.items():
			print(str(rat) + ":" + str(CACHE_AVG_CUSTOMER_RATING[cust_id] - avg) + "," + str(CACHE_AVG_MOVIE_RATING[mov_id] - avg) + "," + str(YEARS_AFTER_RELEASE[mov_id][cust_id]))

if __name__ == "__main__":
	createFile()