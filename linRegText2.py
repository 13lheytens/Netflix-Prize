#!/usr/bin/env python3

import pickle
from Netflix import netflix_predict

with open("caches/tAnswers.p", "rb") as f:
	ANSWERS_CACHE = pickle.load(f)
	f.close()

def printLinRegFormat():
	top_mov_ids = createDictTopMovies()
	for mov_id, cust_arr in ANSWERS_CACHE.items():
		other_movies = {}
		if mov_id in top_mov_ids:
			# Contains dictionary of "related" movies and index
			other_movies = top_mov_ids[mov_id]
		for cust_id, rat in cust_arr.items():
			related_mov_error = [0,0,0]
			for mov , ind in other_movies.items():
				if cust_id in ANSWERS_CACHE[mov]:
					# Difference between predicted and actual rating
					related_mov_error[ind] = netflix_predict(mov, cust_id) - ANSWERS_CACHE[mov][cust_id]
			if related_mov_error != [0,0,0]:
				print(str(rat) + ":" + str(netflix_predict(mov_id, cust_id)) + "," + str(related_mov_error[0]) + "," + str(related_mov_error[1]) + "," + str(related_mov_error[2]))

def createDictTopMovies():
	# Miss Congeniality, Independence Day, Pretty Woman, The Patriot
	# Results from testing Overlap in sample of 5000 customers
	return {5317 : {15124 : 0, 6287: 1, 14313 : 2}, 15124 : {5317 : 0}, 6287 : {5317 : 2}, 14313 : {5317 : 2} }

if __name__ == "__main__":
	printLinRegFormat()