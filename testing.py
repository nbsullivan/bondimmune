import numpy as np
import datetime
from datetime import date
import portfoliofuns
from dateutil.relativedelta import relativedelta
import pandas as pd



if __name__ == '__main__':



	

	# basic long position for a 3-month bond at 5%
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

	

	# testing effective_rate
	effrate = portfoliofuns.effective_rate(position)

	print "effective rate"
	print effrate

	P = portfoliofuns.Pnull(position = position, n = 0)
	print "Pnull value"
	print P

	Positionvalue = portfoliofuns.position_value(position = position, currenttime = 2./12)

	# finding value of bond after 1 month
	print "position value at 1 month bond after."
	print Positionvalue

	# testing out mc_duration calculation.
	mcdur = portfoliofuns.mc_duration(position = position, currenttime = portfoliofuns.date_to_day())

	print "maculay duration."
	print mcdur

	moddur = portfoliofuns.mod_duration(position = position, currenttime = portfoliofuns.date_to_day())

	print "modified duration"
	print moddur


	# testing portfolio duration function.


	# postion 1 same as above 1/3 weight
	position1 = { "weight": 1./3,
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

	# position 2 same as above 1/3 weight
	position2 = { "weight": 1./3,
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

	# position 3 same as above 1/3 weight
	position3 = { "weight": 1./3,
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

	positionlist = [position1, position2, position3]

	portfolio_df = pd.DataFrame(positionlist)

	print "portfolio dataframe"
	print portfolio_df

	print "portfolio dataframe dtypes"
	print portfolio_df.dtypes

	portdur = portfoliofuns.portfolio_duration(portfolio = portfolio_df, Durationtype = 'mc')

	print "portfolio duration:"
	print portdur

	print "this should read \"1962-01-03\""
	print portfoliofuns.day_to_date(daynumber = 1)



