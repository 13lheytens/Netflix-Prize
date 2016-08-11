#!/usr/bin/env python

# -------
# imports
# -------

from helper import Helper

# ----
# main
# ----

if __name__ == "__main__":
    Helper('../linRegText.txt') \
		.with_linear_regression() \
		.with_iterations(1000) \
		.with_term("cust_avg", lambda l: l[0]) \
		.with_term("mov_avg", lambda l: l[1]) \
		.with_term("years_after_release", lambda l: l[2]) \
		.go()

""" #pragma: no cover
"""