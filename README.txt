#NETFLIX PRIZE

The Netflix Prize was an open competition to find the best filtering algorithm for predicting how customers would rate specific movies, given rating data on thousands of movies and customers. A winner was announced in September of 2009 and they were awarded $1,000,000. More information is available at https://en.wikipedia.org/wiki/Netflix_Prize.

In my Software Engineering class (CS 373), we were tasked with the same competition. The goal of our assignment was to design an algorithm that would acheive predictions with a RMSE of less that 1.00.

We were given the following:
	Training Data:
		17,770 movies
		480,189 customers
		about 100,000,000 ratings
		about 5,600 ratings per movie
		about 200 ratings per customer
	Probe Data:
		1,425,333 ratings, all customers from training data
	Movie Data:
		17,770 movies
		Title and year of release for each movie


The Training Data was separated into 17,770 different text files. Each file started with the movie id (followed by a colon), and the following lines each contained a customer id, rating, and date rated

2043:
716091,2,2003-10-02
1990901,5,2001-09-27
1481271,3,2000-09-09
2098867,4,2005-07-12

The Probe Data was one text file containing several movie blocks. Each block started with a movie id (followed by a colon), followed by lines of customer id's. 

2043:
1417435
1828683
818484
10851:
1417435
2312054
462685

The Movie Data was one text file with a movie id, year released, and a title on each line.

2043,1953,Shane
10851,1948,Red River
16306,1960,Spartacus

Our class used the training data to create caches (Python dictionaries) in the form of a pickle file. Examples of the caches are the average customer rating {(int) customer_id : (float) avg_rating} and the average movie rating {(int) movie_id : (float) avg_rating} These caches allowed us to quickly and more accurately predict ratings.

##FILE DESCRIPTIONS:

Netflix.html 			- pydoc results for Netflix.py
Netflix.py 				- utilizes caches to generate predictions (using formula from linear regression)
RunNetflix.in 			- subset of probe data, used for testing
RunNetflix.out 			- prediction results for RunNetflix.in, RMSE printed at bottom
RunNetflix.py 			- uses Netflix.py to solve for predictions, stOut is Predicted Output
TestNetflix.out 		- testing results
TestNetflix.py 			- contains 22 unit tests, testing read, print, predict, rmse, solve, and cache
linRegTest.py 			- outputs individual ratings and cache data in format usable by the gradient-descent code
linRegTest.txt 			- result of linRegTest.py, used to perform linear regression
linRegTest2.py 			- outputs individual ratings and errors in predicting connected movies in format usable by gradient-descent code
makefile 				- used for automated building
probe.out 				- prediction results for probe.txt data, RMSE printed at bottom
probe.txt 				- subset of training data
sampleMovieOverlap.txt 	- results from testMovieOverlap.py
testMovieOverlap.py 	- tests to see how many people have seen a pair of movies, tracks number of pairs and top three pairs

caches/
createCaches.py 		- Creates dictionary caches using given data, dumps caches into pickle files
movYear.p 				- Year in which each movie was released. {(int) movie_id : (int) year_released}
tAnswers.p 				- Training Data Answers {(int) movie_id : {(int) cust_id : (int) actual_rating} }
tAvgCust.p 				- Average Customer Rating from Training Data {(int) customer_id : (float) avg_rating}
tAvgMovie.p 			- Average Movie Rating from Training Data {(int) movie_id : (float) avg_rating}
tYearsSinceRelease.p 	- Contains how many years have passed since movie release at the time of rating 
				  		  { (int) movie_id : {(int) cust_id : (int) years_passed} }
gradient-descent/     
Python 2.7 implementation of Linear and Logistic Regression using Gradient Descent 

Files that I created:
runLinReg.py 		- Runs linear regression on linRegTest.txt using gradient descent (1000 iterations)
linRegResults.txt 	- Results from runLinReg.py, variable names and results at bottom
runLinReg2.py 		- Runs second linear regression on linRegTest2.txt using gradient descent (1000 iterations)
linRegResults2.txt 	- Results from runLinReg2.py, variable names and results at bottom

All other files:
Directly from Github codebox/gradient-descent repository

##PREDICTION APPROACH 1:

Linear Regression with:
1. Overall Average 		- The overall average rating
2. Customer offset		- The amount by which the average rating for a given customer exceeds the overall average
3. Movie offset			- The amount by which the average rating for a given movie exceeds the overall average
4. Years after Release 	- The number of years after the release of the movie (at the time of the rating)

The combination of overall average and the last three variables (with optimal weightings), should produce the following prediction algorithm:
PREDICTED_RATING = OVERALL_AVG + CUSTOMER_OFFSET * w1 + MOVIE_OFFSET * w2 + YEARS_AFTER_RELEASE * w3

Thoughts behind approach:
1. The overall average serves as a good baseline prediction.
2. Customers whose average rating is higher than the overall average are (presumably) more likely to rate any given movie higher than its average.
3. Movies whose average rating is higher than the overall average are (presumably) more likely to be rated higher than the customer average rating.
4. Users may watch a newer movie regardless of whether they think they will like it, and they may be more discriminating in their choice of movie if it is older. This could lead to a higher average movie rating for older movies.

##PREDICTION APPROACH 2:

1. Each movie is similar to other movies to some degree.
2. If I predicted too high or low on other movies I watched, then I maybe be more or less likely to predict high on this movie.

Ideally, I would be able to find the optimal weight for every pair of movies, but this was not realistic for my situation.

How I chose weights:
I figured that the movies with a lot of viewers in common would provide the best weights and benefit the predictions the most.
So, I wrote a python program that iterates through movies that every customer has watched, constructing every possible pair of movies for each customer. A total count of the number of customers that has seen both movies in a pair is kept. The three movie pairs with the highest number of customers ("overlap") is maintained as well.
These three top movie pairs (in a sample of 5000 customers) resulted in the following:
1. Miss Congeniality - Independence Day 
2. Miss Congeniality - Pretty Woman
3. Miss Congeniality - The Patriot

I then ran a linear regression on the result from the first prediction approach, combined with errors in rating these pairs of movies.

The actual benefit to this approach was minimal, but given more time and resources, more combinations can be discovered and utilized.




