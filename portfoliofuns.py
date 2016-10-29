import pandas as pd
import numpy as np

	"""
	portfolio_df structure:

	weight: percentage of portfolio invested in position, float < 1
	positiontype: either "long" or "short", string
	bondtype: 1-month	3-month	6-month	1-year	2-year	3-year	5-year	7-year	10-year	20-year	30-year, string
	interestrate: annual interest rate, float
	maturitydate: date of maturity, datetime64

	position dictionary strcture: (same as a row in the portfolio dataframe)

	weight: percentage of portfolio invested in position, float
	positiontype: either "long" or "short", string
	bondtype: 1-month	3-month	6-month	1-year	2-year	3-year	5-year	7-year	10-year	20-year	30-year, string
	interestrate: annual interest rate, float
	maturitydate: date of maturity, datetime64
	"""

	
def mc_duration(position = None):
	"""
	Macaulay Duration of a position
	"""

	return None

def asset_procceds(portfolio = None):
	"""
	asset procceds of a portfolio
	"""

	return None

def liability_outgo(portfolio = None):
	"""
	liability-outgo of a portfolio
	"""

	return None

def position_value(position = None):
	"""
	calculate the value of a position, can accept long and short positions
	"""

	if position["positiontype"] == 'short':
		# do something

	if position["positiontype"] == 'long':
		# do something

	else:
		print "bad positiontype"

	return None


