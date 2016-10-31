import pandas as pd
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta

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

some other notes:
in position_value currenttime is a float representing number of years?
in mc_duration currenttime is a datetime64 object.
"""

	
def mc_duration(position = None, currenttime = None):
	"""
	Macaulay Duration of a position, returns the durantion as a number of years (float).
	"""

	# get dates and payments this is moot for zero coupon bonds.
	dates = position["coupondates"]
	payments = position["couponpayments"]

	# make the t_j - t_0 terms
	offsetdates = dates - currenttime

	# get it out of timedelta datatypes, note this is terms of days
	offsetdatesunitless = np.array((offsetdates/ np.timedelta64(1, 'D')) / 365 )

	# do the same things with the dates. also they are in terms of days.
	datesunitless = np.array(((dates - position["createdate"]) / np.timedelta64(1, 'D')) / 365)

	# note things are not happy when we are doing this days and years do not have the same base unit, this assume we are not in a leap year
	Pjslist = [position_value(position = position, currenttime = b) for (a,b) in np.ndenumerate(offsetdatesunitless)]

	macdur = np.sum(Pjslist * offsetdatesunitless) / np.sum(Pjslist * datesunitless)

	effectiverate, timeperiod = effective_rate(position = position)

	# change the unit of macdur to the time period of the bond.
	macdur = macdur * timeperiod

	return macdur

def asset_procceds(portfolio = None):
	"""
	asset procceds of a portfolio
	"""

	############### TODO ################

	return None

def liability_outgo(portfolio = None):
	"""
	liability-outgo of a portfolio
	"""

	############### TODO ################

	return None

def position_value(position = None, currenttime = None):
	"""
	calculate the value of a position, can accept long and short positions.
	returns position value based on derivates market book
	"""

	if position["positiontype"] == 'short':
		pass
		# do something

	if position["positiontype"] == 'long':
		"""
		based on derriavitives market book page 209 equation 7.4
		"""
		effrate, timeperiod = effective_rate(position = position)
		t0price = Pnull(position = position, n = currenttime)
		t1price = Pnull(position = position, n = timeperiod)
		posvalue = t1price / t0price

	else:
		print "bad positiontype"
		return None

	return posvalue

def Pnull(position = None, n = None):
	"""
	gives P(0,n) as defined by derivatives market page 208 equation 7.1
	"""

	effrate, timeperiod = effective_rate(position)

	P = 1.0 / ((1 + effrate) ** n)

	return P

def effective_rate(position = None):
	"""
	return effective rate and time period of bond, given a bondtype and interestrate as defined above.
	"""
	bondtype = position["bondtype"]
	interestrate = position["interestrate"]

	if "month" in bondtype:

		months = int(str.split(bondtype, "-")[0])
		devisor = 12/ months
		effectiverate = interestrate/devisor

		# time period is the length of time used in other functionss
		timeperiod = float(months) / 12
	
	elif "year" in bondtype:

		years = int(str.split(bondtype, "-")[0])
		effectiverate = (1 + interestrate)**years

		timeperiod = years



	return effectiverate, timeperiod
									
