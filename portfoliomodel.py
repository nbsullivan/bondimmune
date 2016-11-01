import pandas as pd
import numpy as np

if __name__ == '__main__':
	

	"""
	portfolio_df structure:

	weight: percentage of portfolio invested in position, float < 1
	positiontype: either "long" or "short", string
	bondtype: 1-month	3-month	6-month	1-year	2-year	3-year	5-year	7-year	10-year	20-year	30-year, string
	interestrate: annual interest rate, 5% = .05, float
	maturitydate: date of maturity, datetime64
	coupondates: dates of coupon payments, if zero coupon simply the maturity date, list of datetime64
	couponpayments: payment amounts for coupon dates list of dollar amounts

	position dictionary strcture: (same as a row in the portfolio dataframe)

	weight: percentage of portfolio invested in position, float
	positiontype: either "long" or "short", string
	bondtype: 1-month	3-month	6-month	1-year	2-year	3-year	5-year	7-year	10-year	20-year	30-year, string
	interestrate: annual interest rate, 5% = .05, float
	maturitydate: date of maturity, datetime64
	coupondates: dates of coupon payments, if zero coupon simply the maturity date, list of datetime64
	couponpayments: payment amounts for coupon dates list of dollar amounts
	"""
	portfolio_df = pd.DataFrame(columns = ['weight', 'positiontype', 'bondtype', 'interestrate', 'maturitydate'])




	position_dict = { "weight": 1,
				 	  "positiontype": "long",
				 	  "bondtype" : "1-year",
				 	  "interestrate" : .05,
				 	  "createdate" : np.datetime64(date.today()),
				 	  "maturitydate" : np.datetime64(date.today() + relativedelta(years=1)),
				 	  "coupondates" : np.array(np.datetime64(date.today() + relativedelta(years=1))),
				 	  "couponpayments" : np.array(1.05) }


	"""
	Consistentency of these conventions will be import.
	"""

	
