#!/usr/bin/env python3

import pickle
from Netflix import netflix_predict

with open("caches/tAnswers.p", "rb") as f:
	ANSWERS_CACHE = pickle.load(f)
	f.close()

def createFile():

	top_mov_ids = createDictTopMovies()
	for mov_id, cust_arr in ANSWERS_CACHE.items():
		other_movies = []
		if str(mov_id) in top_mov_ids:
			other_movies = top_mov_ids[str(mov_id)]
		for cust_id, rat in cust_arr.items():
			related_mov_error = [0, 0, 0]
			if len(other_movies) == 3:
				for i in range(3):
					if cust_id in ANSWERS_CACHE[top_mov_ids[str(mov_id)][i]]:
						related_mov_error[i] = netflix_predict(top_mov_ids[str(mov_id)][i], cust_id) - ANSWERS_CACHE[top_mov_ids[str(mov_id)][i]][cust_id]
				if related_mov_error != [0,0,0]:
					print(str(rat) + ":" + str(netflix_predict(mov_id, cust_id)) + "," + str(related_mov_error[0]) + "," + str(related_mov_error[1]) + "," + str(related_mov_error[2]))
			elif len(other_movies) == 1 and cust_id in ANSWERS_CACHE[top_mov_ids[str(mov_id)][0]]:
				if mov_id == 15124:
					related_mov_error[0] = netflix_predict(top_mov_ids[str(mov_id)][0], cust_id) - ANSWERS_CACHE[top_mov_ids[str(mov_id)][0]][cust_id]
				elif mov_id == 6287:
					related_mov_error[1] = netflix_predict(top_mov_ids[str(mov_id)][0], cust_id) - ANSWERS_CACHE[top_mov_ids[str(mov_id)][0]][cust_id]
				elif mov_id == 14313:
					related_mov_error[2] = netflix_predict(top_mov_ids[str(mov_id)][0], cust_id) - ANSWERS_CACHE[top_mov_ids[str(mov_id)][0]][cust_id]
				print(str(rat) + ":" + str(netflix_predict(mov_id, cust_id)) + "," + str(related_mov_error[0]) + "," + str(related_mov_error[1]) + "," + str(related_mov_error[2]))
			#print(str(rat) + ":" + str(netflix_predict(mov_id, cust_id)) + "," + str(related_mov_error[0]) + "," + str(related_mov_error[1]) + "," + str(related_mov_error[2]))

def createDictTopMovies():
	# Miss Congeniality, Independence Day, Pretty Woman, The Patriot
	return {"5317" : [15124, 6287, 14313], "15124" : [5317], "6287" : [5317], "14313" : [5317]} 

if __name__ == "__main__":
	createFile()