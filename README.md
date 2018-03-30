# NETFLIX PRIZE

The Netflix Prize was an open competition to find the best filtering algorithm for predicting how customers would rate specific movies, given rating data on thousands of movies and customers. A winner was announced in September of 2009 and they were awarded $1,000,000. More information is available at https://en.wikipedia.org/wiki/Netflix_Prize.

In my Software Engineering class (CS 373), we were tasked with the same competition. The goal of our assignment was to design an algorithm that would acheive predictions with a RMSE of less that 1.00.

*We were given the following*:

**Training Data**:

<ul>
<li>17,770 movies</li>
<li>480,189 customers</li>
<li>about 100,000,000 ratings</li>
<li>about 5,600 ratings per movie</li>
<li>about 200 ratings per customer</li>
</ul>

**Probe Data**:

<ul>
<li>1,425,333 ratings</li>
<li>subset of training data used to test prediction algorithms</li>
</ul>

**Movie Data**:

<ul>
<li>17,770 movies</li>
<li>Title and year of release for each movie</li>
</ul>


The Training Data was separated into four different text files. Each file started with the movie id (followed by a colon), and the following lines each contained a customer id, rating, and date rated for that movie. More movie blocks followed. Each of the four files contained approximately an equal number of movies.

<pre>
2043:
716091,2,2003-10-02
1990901,5,2001-09-27
1481271,3,2000-09-09
2098867,4,2005-07-12
</pre>

The Probe Data was structured like the training data. Each movie block started with a movie id (followed by a colon), followed by lines of customer id's. 

<pre>
2043:
1417435
1828683
818484
10851:
1417435
2312054
462685
</pre>

The Movie Data was one text file with a movie id, year released, and a title on each line.

<pre>
2043,1953,Shane
10851,1948,Red River
16306,1960,Spartacus
</pre>

I used the training data to create caches (Python dictionaries) in the form of a pickle file. Examples of the caches are the average customer rating *{(int) customer_id : (float) avg_rating}* and the average movie rating *{(int) movie_id : (float) avg_rating}* These caches allowed me to quickly and more accurately predict ratings.

## FILE DESCRIPTIONS:

*Netflix.py* 				- utilizes caches to generate predictions

*RunNetflix.in* 			- subset of probe data, used for testing

*RunNetflix.out* 			- prediction results for RunNetflix.in, RMSE printed at bottom

*RunNetflix.py* 			- uses Netflix.py to solve for predictions

*TestNetflix.out*	 		- testing results

*TestNetflix.py* 			- contains 22 unit tests, testing read, print, predict, rmse, solve, and cache

*makefile*				- used for automated building

*probe.out*				- prediction results for probe.txt data, RMSE printed at bottom

*probe.txt*				- subset of training data

**caches/**

*createCaches.py* 		- Creates dictionary caches using given data, dumps caches into pickle files

*movieYears.p* 				- Year in which each movie was released {(int) movie_id : (int) year_released}

*ratingsMovies.p* 			- Training Data Ratings {(int) movie_id : {(int) cust_id : (int) actual_rating} }

*ratingsCustomers.p* 		- Training Data Ratings {(int) cust_id : {(int) movie_id : (int) actual_rating} }

*avgCustomerRatings.p* 		- Average Customer Rating from Training Data {(int) customer_id : (float) avg_rating}

*avgMovieRatings.p* 		- Average Movie Rating from Training Data {(int) movie_id : (float) avg_rating}

*yearsSinceRelease.p* 	- Contains how many years have passed since movie release at the time of rating 
				  		  { (int) movie_id : {(int) cust_id : (int) years_passed} }

*moviePredictionErrorCorrelations.p* 	- Contains correlations between prediction (Approach 1) errors of the three top watched movies. Example: For each customer, if prediction Approach 1 tends err in the same direction (guess above/below actual rating) for a pair of movies, the correlation would be positive. { (int) movie_id : {(int) movie_id : (float) correlation} }

## PREDICTION APPROACH 1:

1. Overall Average 		- The overall average rating of all movies and customers
2. Customer offset		- The amount by which the average rating for a given customer exceeds the overall average
3. Movie offset			- The amount by which the average rating for a given movie exceeds the overall average

*PREDICTED_RATING = OVERALL_AVG + CUSTOMER_OFFSET + MOVIE_OFFSET*

Thoughts behind approach:

1. The overall average serves as a good baseline prediction.
2. Customers whose average rating is higher than the overall average are (presumably) more likely to rate any given movie higher than its average.
3. Movies whose average rating is higher than the overall average are (presumably) more likely to be rated higher than the customer average rating.

## PREDICTION APPROACH 2:

1. Each movie is similar to other movies to some degree.
2. If prediction approach 1 was too high (or low) on other movies I watched, then based on how similar the movies are to one another, approach 1 may be likely to predict high (or low) on this movie.

I used the correlations between the prediction approach 1 errors of the top 3 most watched movies to enhance prediction approach 1.

*APPROACH_2_OFFSET = CORRELATION(OTHER_MOVIE_WATCHED, THIS_MOVIE) * OTHER_MOVIE_PREDICTION_ERROR*

*PREDICTED_RATING = OVERALL_AVG + CUSTOMER_OFFSET + MOVIE_OFFSET + APPROACH_2_OFFSET*

The actual benefit to this approach was minimal, but given more time and resources, more correlations can be calculated and utilized.

## FUTURE APPROACH:

1. Add more (or all) movie pair correlations
2. Incorporate Customer pair correlations (similar to movie pair correlations)


