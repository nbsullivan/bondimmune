import pandas as pd
import numpy as np

if __name__ == '__main__':
	

	"""
	portfolio_list structure:

	A list of position dictionary


	position dictionary strcture: (same as a row in the portfolio dataframe)

	position = { "weight": 100,
				 "positiontype": "long",
				 "bondtype" : "3-month",
				 "interestrate" : .05,
				 "createdate" : portfoliofuns.date_to_day(date.today()),
				 "maturitydate" : portfoliofuns.date_to_day(date.today() + relativedelta(months=3)),
				 "coupondates" : np.array([portfoliofuns.date_to_day(date.today() + relativedelta(months=1)),
				 							portfoliofuns.date_to_day(date.today() + relativedelta(months=2)),
				 							portfoliofuns.date_to_day(date.today() + relativedelta(months=3)), 
				 							portfoliofuns.date_to_day(date.today() + relativedelta(months=3))]),
				 "couponpayments" : np.array([10, 10, 10, 100]) }


	"""
	"""
	Consistentency of these conventions will be import.
	"""

	
