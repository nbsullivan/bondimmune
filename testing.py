import numpy as np
import datetime
from datetime import date
import portfoliofuns
from dateutil.relativedelta import relativedelta



if __name__ == '__main__':


	# basic long position for a 1-month bond	
	position = { "weight": 1,
				 "positiontype": "long",
				 "bondtype" : "3-month",
				 "interestrate" : .05,
				 "maturitydate" : np.datetime64(date.today() + relativedelta(months=1)),
				 "coupondates" : [np.datetime64(date.today() + relativedelta(months=1))],
				 "couponpayments" : [1.05] }

	# testing out mc_duration calculation.
	mcdur = portfoliofuns.mc_duration(position)

	# testing effective_rate
	effrate, timeperiod = portfoliofuns.effective_rate(position)

	print "effective rate and time period"
	print effrate, timeperiod

	P = portfoliofuns.Pnull(position = position, n = 1/4)

	print "Pnull value"
	print P