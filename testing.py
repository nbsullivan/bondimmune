import numpy as np
import datetime
from datetime import date
import portfoliofuns
from dateutil.relativedelta import relativedelta
import pandas as pd




if __name__ == '__main__':



	dt_str = '1/1/2016'

	startdate = datetime.datetime.strptime(dt_str, "%m/%d/%Y").date()
	

	position = { "weight": 1,
				 "positiontype": "long",
				 "bondtype" : "6-month",
				 "interestrate" : .046,
				 "createdate" : portfoliofuns.date_to_day(startdate),
				 "maturitydate" : portfoliofuns.date_to_day(startdate + relativedelta(months=6)),
				 "coupondates" : np.array([portfoliofuns.date_to_day(startdate + relativedelta(months=2)),
				 							portfoliofuns.date_to_day(startdate + relativedelta(months=4)),
				 							portfoliofuns.date_to_day(startdate + relativedelta(months=6)), 
				 							portfoliofuns.date_to_day(startdate + relativedelta(months=6)),]),
				 "couponpayments" : np.array([70, 70, 70, 1000]),
				 "payperyear" : 6 }

	

	# testing effective_rate
	effrate = portfoliofuns.effective_rate(position)

	print "effective rate"
	print effrate


	currenttime = portfoliofuns.date_to_day(startdate)
	Positionvalue = portfoliofuns.position_value(position = position, currenttime = currenttime)

	print "position value at creation time of bond."
	print Positionvalue
	
	# testing out mc_duration calculation.
	mcdur = portfoliofuns.mc_duration(position = position, currenttime = currenttime)

	print "maculay duration."
	print mcdur

	moddur = portfoliofuns.mod_duration(position = position, currenttime = currenttime)

	print "modified duration"
	print moddur


	# testing portfolio duration function.

	"""
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


	print "testing grabing interestrate data from the dataset"
	print portfoliofuns.todays_rates(daynumber = 0)
	"""




