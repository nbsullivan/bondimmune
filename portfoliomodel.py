import pandas as pd
import numpy as np

if __name__ == '__main__':
	

	"""
	portfolio_df structure:
	weight: percentage of portfolio invested in position, float < 1
	positiontype: either "long" or "short", string
	bondtype: 1-month	3-month	6-month	1-year	2-year	3-year	5-year	7-year	10-year	20-year	30-year, string
	interestrate: annual interest rate, float
	maturitydate: date of maturity, datetime64
	"""
	portfolio_df = pd.DataFrame(columns = ['weight', 'positiontype', 'bondtype', 'interestrate', 'maturitydate'])


	"""
	position dictionary strcture: (same as a row in the portfolio dataframe)
	weight: percentage of portfolio invested in position, float
	positiontype: either "long" or "short", string
	bondtype: 1-month	3-month	6-month	1-year	2-year	3-year	5-year	7-year	10-year	20-year	30-year, string
	interestrate: annual interest rate, float
	maturitydate: date of maturity, datetime64
	"""

	position_dict = {"weight" : 0, 
					 "positiontype" : "long",
					 "bondtype" : "1-month",
					 "interestrate" : 1.00,
					 "maturitydate" : np.datetime64('2016-11-29') }


	"""
	Consistentency of these conventions will be import.
	"""
