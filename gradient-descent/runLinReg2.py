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
		.with_iterations(1000) \
		.with_term("predicted_val", lambda l: l[0]) \
		.with_term("Miss_Indep", lambda l: l[1]) \
		.with_term("Miss_Pretty", lambda l: l[2]) \
		.with_term("Miss_Patrit", lambda l: l[3]) \
		.go()

""" #pragma: no cover
"""