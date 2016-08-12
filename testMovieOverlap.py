#!/usr/bin/env python3


import pickle


def loadAnswersCache():
	with open("../Desktop/tAnswers.p", "rb") as f:
		CACHE_ANSWERS = pickle.load(f)
		f.close()
	return CACHE_ANSWERS



def getCustFirstCache(CACHE_ANSWERS):
	CACHE_CUST_FIRST = {}
	for mov_id, cust_dict in CACHE_ANSWERS.items():
		for cust_id, rat in cust_dict.items():
			if not cust_id in CACHE_CUST_FIRST:
				CACHE_CUST_FIRST[cust_id] = []
			CACHE_CUST_FIRST[cust_id] += [mov_id]
	return CACHE_CUST_FIRST



def printMovieOverlap(CACHE_CUST_FIRST):
	count_customers = 0
	sample_step = 100
	top_three_overlap = []
	CACHE_MOV_OVERLAP = {}

	for cust_id, mov_arr in CACHE_CUST_FIRST.items():
		if len(top_three_overlap) == 0:
			first = str(mov_arr[0]) + "_" + str(mov_arr[1])
			top_three_overlap = [first, first, first]
		count_customers += 1
		for i in range(len(mov_arr)):
			for j in range(i+1, len(mov_arr)):
				x = str(mov_arr[i]) + "_" + str(mov_arr[j])
				y = str(mov_arr[j]) + "_" + str(mov_arr[i])
				if x in CACHE_MOV_OVERLAP:
					CACHE_MOV_OVERLAP[x] += 1
					top_three_overlap = updateTop(top_three_overlap,CACHE_MOV_OVERLAP, x)
				elif y in CACHE_MOV_OVERLAP:
					CACHE_MOV_OVERLAP[y] += 1
					top_three_overlap = updateTop(top_three_overlap,CACHE_MOV_OVERLAP, y)
				else:
					CACHE_MOV_OVERLAP[x] = 1
		if (count_customers % sample_step == 0):
			print("In a sample of " + str(count_customers) + " customers, we found:")
			print("   Total Movie overlaps: " + str(len(CACHE_MOV_OVERLAP)))
			print("   Num Overlaps for " + str(top_three_overlap[0]) + ": " + str(CACHE_MOV_OVERLAP[top_three_overlap[0]]))
			print("   Num Overlaps for " + str(top_three_overlap[1]) + ": " + str(CACHE_MOV_OVERLAP[top_three_overlap[1]]))
			print("   Num Overlaps for " + str(top_three_overlap[2]) + ": " + str(CACHE_MOV_OVERLAP[top_three_overlap[2]]))
			print()

def updateTop(top_three_overlap, CACHE_MOV_OVERLAP, x):
	if x == top_three_overlap[2]:
		if (CACHE_MOV_OVERLAP[x] > CACHE_MOV_OVERLAP[top_three_overlap[1]]):
			top_three_overlap[2] = top_three_overlap[1]
			top_three_overlap[1] = x
	elif x == top_three_overlap[1]:
		if (CACHE_MOV_OVERLAP[x] > CACHE_MOV_OVERLAP[top_three_overlap[0]]):
			top_three_overlap[1] = top_three_overlap[0]
			top_three_overlap[0] = x
	elif x != top_three_overlap[0]:
		if (CACHE_MOV_OVERLAP[x] > CACHE_MOV_OVERLAP[top_three_overlap[2]]):
			top_three_overlap[2] = x
	return top_three_overlap

if __name__ == "__main__":
	CACHE_ANSWERS = loadAnswersCache()
	print("Finished Loading Answers Cache")
	CACHE_CUST_FIRST = getCustFirstCache(CACHE_ANSWERS)
	print("Finished creating Customer First cache")
	printMovieOverlap(CACHE_CUST_FIRST)