#!/usr/bin/env python3
""" NETFLIX TESTS
"""
# -------
# imports
# -------

import pickle
from io import StringIO
from unittest import main, TestCase

from Netflix import netflix_read, netflix_print, \
    netflix_predict, netflix_rmse, netflix_solve

# -----------
# TestNetflix
# -----------

class TestNetflix(TestCase):

    # ----
    # read
    # ----

    def test_read_1(self):
        """ tests reading movie_id:
        """
        line = "2043:\n"
        val, ind = netflix_read(line)
        self.assertEqual(val, 2043)
        self.assertEqual(ind, 1)

    def test_read_2(self):
        """ tests reading customer_id
        """
        line = "1417435\n"
        val, ind = netflix_read(line)
        self.assertEqual(val, 1417435)
        self.assertEqual(ind, 0)

    def test_read_3(self):
        """ test reading empty line
        """
        line = "\n"
        val, ind = netflix_read(line)
        self.assertEqual(val, -1)
        self.assertEqual(ind, -1)

    # -----
    # print
    # -----

    def test_print_1(self):
        """ tests printing rating
        """
        rating = 1.0
        writer = StringIO()
        netflix_print(writer, rating)
        self.assertEqual(writer.getvalue(), "1.0\n")

    def test_print_2(self):
        """ tests printing movie_id
        """
        rating = 2043
        writer = StringIO()
        netflix_print(writer, rating)
        self.assertEqual(writer.getvalue(), "2043:\n")

    def test_print_3(self):
        """ tests printing RMSE
        """
        rating = "RMSE: 0.93"
        writer = StringIO()
        netflix_print(writer, rating)
        self.assertEqual(writer.getvalue(), "RMSE: 0.93\n")

    # ----
    # cache
    # ----

    def test_cache_1(self):
        """
        tests opening movYear cache
        tests movYear cache vals
        """
        with open("caches/movYear.p", "rb") as cache:
            mov_year_cache = pickle.load(cache)
            cache.close()
        self.assertEqual(mov_year_cache[94], 2000)
        self.assertEqual(mov_year_cache[12711], 1952)
        self.assertEqual(mov_year_cache[12755], 1995)

    def test_cache_2(self):
        """
        tests opening tAnswers cache
        tests tAnswers cache vals
        """
        with open("caches/tAnswers.p", "rb") as cache:
            answers_cache = pickle.load(cache)
            cache.close()
        self.assertEqual(answers_cache[2043][814483], 4)
        self.assertEqual(answers_cache[10][1952305], 3)
        self.assertEqual(answers_cache[10017][2280428], 3)

    def test_cache_3(self):
        """
        tests opening tAvgCust cache
        tests tAvgCust cache vals
        """
        with open("caches/tAvgCust.p", "rb") as cache:
            avg_cust_cache = pickle.load(cache)
            cache.close()
        self.assertEqual(avg_cust_cache[814483], 3.6666666666666665)
        self.assertEqual(avg_cust_cache[1952305], 3.409340659340659)
        self.assertEqual(avg_cust_cache[2280428], 3.72)

    def test_cache_4(self):
        """
        tests opening tAvgMovie cache
        tests tAvgMovie cache vals
        """
        with open("caches/tAvgMovie.p", "rb") as cache:
            avg_movie_cache = pickle.load(cache)
            cache.close()
        self.assertEqual(avg_movie_cache[2043], 3.7776648456358783)
        self.assertEqual(avg_movie_cache[10], 3.180722891566265)
        self.assertEqual(avg_movie_cache[10017], 2.982142857142857)

    def test_cache_5(self):
        """
        tests opening tYearsSinceRelease cache
        tests tYearsSinceRelease cache vals
        """
        with open("caches/tYearsSinceRelease.p", "rb") as cache:
            years_since_release_cache = pickle.load(cache)
            cache.close()
        self.assertEqual(years_since_release_cache[2043][716091], 50)
        self.assertEqual(years_since_release_cache[1000][2326571], 2)
        self.assertEqual(years_since_release_cache[10001][262828], 11)

    #-----
    # rmse
    # -----

    def test_solve_1(self):
        """ test solves input 1"""
        inp = StringIO("2043:\n1417435\n2312054\n462685\n")
        writer = StringIO()
        netflix_solve(inp, writer)
        self.assertEqual(
            writer.getvalue(), "2043:\n3.7\n4.6\n4.0\nRMSE: 2.1283858730975753\n")

    def test_solve_2(self):
        """ test solves input 2"""
        inp = StringIO("1:\n30878\n2043:\n462685\n")
        writer = StringIO()
        netflix_solve(inp, writer)
        self.assertEqual(
            writer.getvalue(), "1:\n3.7\n2043:\n4.0\nRMSE: 0.18432622758011358\n")

    def test_solve_3(self):
        """ test solves input 3"""
        inp = StringIO("2043:\n2312054\n1:\n30878\n")
        writer = StringIO()
        netflix_solve(inp, writer)
        self.assertEqual(
            writer.getvalue(), "2043:\n4.6\n1:\n3.7\nRMSE: 2.5588590159754325\n")

    def test_solve_4(self):
        """ test solves invalid input 4"""
        inp = StringIO("2043:\n2312054\n1:\n\n")
        writer = StringIO()
        with self.assertRaises(AssertionError):
            netflix_solve(inp, writer)

    # -------
    # predict
    # -------

    def test_predict_1(self):
        """ test predicts movie and customer"""
        movie_id = 1
        customer_id = 30878
        res = netflix_predict(movie_id, customer_id)
        self.assertEqual(res, 3.7394321383123703)

    def test_predict_2(self):
        """ test predicts movie and customer"""
        movie_id = 10
        customer_id = 1952305
        res = netflix_predict(movie_id, customer_id)
        self.assertEqual(res, 3.020308046060214)

    def test_predict_3(self):
        """ test predicts movie and customer"""
        movie_id = 1002
        customer_id = 2174660
        res = netflix_predict(movie_id, customer_id)
        self.assertEqual(res, 3.2379678434646615)

    # -----
    # rmse
    # -----

    def test_rmse_1(self):
        """ tests rmse function"""
        ans = [2, 3, 4]
        pre = [2, 3, 4]
        res = netflix_rmse(ans, pre)
        self.assertEqual(res, 0.0)

    def test_rmse_2(self):
        """ tests rmse function"""
        ans = [2, 3, 4]
        pre = [3, 2, 3]
        res = netflix_rmse(ans, pre)
        self.assertEqual(res, 1.0)

    def test_rmse_3(self):
        """ tests rmse function"""
        ans = [2, 3, 4]
        pre = [4, 3, 2]
        res = netflix_rmse(ans, pre)
        self.assertEqual(res, 1.632993161855452)

    def test_rmse_4(self):
        """ tests rmse function on dictionaries"""
        ans_cust = {123: 3, 234: 4}
        pre_cust = {123: 4, 234: 5}
        ans = {2034: ans_cust, 2345: ans_cust}
        pre = {2034: pre_cust, 2345: pre_cust}
        res = netflix_rmse(ans, pre)
        self.assertEqual(res, 1.0)


# ----
# main
# ----

if __name__ == "__main__":
    main()

