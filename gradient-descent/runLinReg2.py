#!/usr/bin/env python

# -------
# imports
# -------

from helper import Helper

# ----
# main
# ----

if __name__ == "__main__":
    Helper('../linRegText2.txt') \
		.with_linear_regression() \
		.with_iterations(2000) \
		.with_term("5317_15124", lambda l: l[0]) \
		.with_term("5317_6287", lambda l: l[1]) \
		.with_term("5317_14313", lambda l: l[2]) \
		.go()

""" #pragma: no cover
"""