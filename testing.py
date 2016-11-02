import numpy as np
import datetime
from datetime import date
import portfoliofuns
from dateutil.relativedelta import relativedelta
import pandas as pd



if __name__ == '__main__':


	# basic long position for a 3-month bond at 5%
	position = { "weight": 1,
				 "positiontype": "long",
				 "bondtype" : "3-month",
				 "interestrate" : .05,
				 "createdate" : np.datetime64(date.today()),
				 "maturitydate" : np.datetime64(date.today() + relativedelta(months=3)),
				 "coupondates" : np.array(np.datetime64(date.today() + relativedelta(months=3))),
				 "couponpayments" : np.array(1.05) }

	

	# testing effective_rate
	effrate = portfoliofuns.effective_rate(position)

	print "effective rate"
	print effrate

	P = portfoliofuns.Pnull(position = position, n = 1)
	print "Pnull value"
	print P

	Positionvalue = portfoliofuns.position_value(position = position, currenttime = 1./12)

	# finding value of bond after 1 month
	print "position value at 1 month bond after."
	print Positionvalue


	# testing out mc_duration calculation.
	mcdur = portfoliofuns.mc_duration(position = position, currenttime = np.datetime64(date.today()))

	print "maculay duration."
	print mcdur

	moddur = portfoliofuns.mod_duration(position = position, currenttime = np.datetime64(date.today()))

	print "modified duration"
	print moddur


	# testing portfolio duration function.

	# postion 1 same as above .25 weight
	position1 = { "weight": .25,
			 "positiontype": "long",
			 "bondtype" : "3-month",
			 "interestrate" : .05,
			 "createdate" : np.datetime64(date.today()),
			 "maturitydate" : np.datetime64(date.today() + relativedelta(months=3)),
			 "coupondates" : np.array(np.datetime64(date.today() + relativedelta(months=3))),
			 "couponpayments" : np.array(1.05)}

	# position 2 1 year bond at 4% .5 weight
	position2 = { "weight": .5,
				 "positiontype": "long",
				 "bondtype" : "1-year",
				 "interestrate" : .04,
				 "createdate" : np.datetime64(date.today()),
				 "maturitydate" : np.datetime64(date.today() + relativedelta(years=1)),
				 "coupondates" : np.array(np.datetime64(date.today() + relativedelta(years=1))),
				 "couponpayments" : np.array(1.04)}

	# position 3 5 year bond at 4.5% .25 weight
	position3 = { "weight": .25,
				 "positiontype": "long",
				 "bondtype" : "3-year",
				 "interestrate" : .045,
				 "createdate" : np.datetime64(date.today()),
				 "maturitydate" : np.datetime64(date.today() + relativedelta(years=3)),
				 "coupondates" : np.array(np.datetime64(date.today() + relativedelta(years=3))),
				 "couponpayments" : np.array(1.045)}

	positionlist = [position1, position2, position3]

	portfolio_df = pd.DataFrame(positionlist)

	print "portfolio dataframe"
	print portfolio_df

	print "portfolio dataframe dtypes"
	print portfolio_df.dtypes

	portdur = portfoliofuns.portfolio_duration(portfolio = portfolio_df, Durationtype = 'mc')

	print "portfolio duration:"
	print portdur




