import pandas as pd
import numpy as np
import datetime
from datetime import date
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

	# handle default case for current time
	if currenttime == None:
		currenttime = date_to_day()

	print "currenttime"
	print currenttime

	# make the t_j - t_0 terms
	offsetdates = (dates - currenttime) / 365


	# do the same things with the dates. also they are in terms of days.
	datesunitless = (dates - position["createdate"]) / 365

	# note things are not happy when we are doing this days and years do not have the same base unit, this assume we are not in a leap year
	Pjslist = np.array([position_value(position = position, currenttime = b) for (a,b) in np.ndenumerate(offsetdates)])

	macdur = np.sum(Pjslist * offsetdates) / np.sum(Pjslist * datesunitless)

	# grab time period for scaling duration
	timeperiod = timeper(position = position)


	# change the unit of macdur to the time period of the bond.
	macdur = macdur * timeperiod

	return macdur


def mod_duration(position = None, currenttime = None):

	macdur = mc_duration(position = position, currenttime = currenttime)
	effrate = effective_rate(position = position)

	moddur = macdur / (((effrate - 1)/position["coupondates"].size) + 1)


	return moddur




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
		# get effective rate and time period
		effrate = effective_rate(position = position)
		timeperiod = timeper(position = position)

		t0price = Pnull(position = position, n = currenttime)
		t1price = Pnull(position = position, n = timeperiod)

		posvalue = t0price / t1price

	else:
		print "bad positiontype"
		return None

	return posvalue

def Pnull(position = None, n = None):
	"""
	gives P(0,n) as defined by derivatives market page 208 equation 7.1
	"""

	# we are getting effective rate for the time period of the whole bond not yearly
	effrate = effective_rate(position)

	timeperiod = timeper(position)


	Pc = position["couponpayments"] 
	tc = position["coupondates"] - position["createdate"]

	PV = np.sum(Pc/(effrate**tc))

	return PV



def timeper(position = None):
	"""
	return effective rate and time period of bond, given a bondtype and interestrate as defined above.
	"""
	bondtype = position["bondtype"]
	interestrate = position["interestrate"]

	if "month" in bondtype:

		months = int(str.split(bondtype, "-")[0])
		devisor = 12/ months

		# time period is the length of time used in other functionss
		timeperiod = float(months) / 12
		
	elif "year" in bondtype:

		years = int(str.split(bondtype, "-")[0])

		timeperiod = years



	return timeperiod

def effective_rate(position = None):
	"""
	effective rate for a bond, this also might be YTM
	"""

	# get interest rate and time period of possition
	interestrate = position["interestrate"]
	timeperiod = timeper(position)

	effectiverate = (1 + interestrate)**(1./365)

	return effectiverate


def portfolio_duration(portfolio = None, Durationtype = 'mc', currenttime = None):
	"""
	has not been tested yet.
	"""

	portfolio_list = portfolio.to_dict('records')

	# holder for duration value

	for position in portfolio_list:

		# calculate duration based on desirsed type
		if Durationtype == 'mc':
		
			# macaulay duration
			position["duration"] = mc_duration(position = position, currenttime = currenttime)

		elif Durationtype == 'md':

			# modified duration
			position['duration'] = mod_duration(position = position, currenttime = currenttime)

		else:

			# if a bad type is entered use mc_dur
			print "bad duration type entered, using macaulay duration"

			position["duration"] = mc_duration(position = position, currenttime = currenttime)


	# reconsistute df.
	portfolio_dur_df = pd.DataFrame(portfolio_list)

	portduration = np.sum(portfolio_dur_df["duration"] * portfolio_dur_df["weight"])

	return portduration


def date_to_day(datetimeobj = None):
	"""
	Converts dates into integers, day 0: 1962-01-02
	"""

	# epoch: start of fed reserve dataset
	epoch = date(1962, 1, 2)

	# make sure a date is actaully passed, if none is passed return the value of today
	if datetimeobj == None:

		datetimeobj = date.today()

	delta = datetimeobj - epoch
	days = delta.days
	return days


def day_to_date(daynumber = None):
	"""
	converts a day number to a datetime.date object
	"""

	epoch = date(1962, 1, 2)

	if daynumber == None:
		print "no day given"
		return None











									
