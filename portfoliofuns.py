import pandas as pd
import numpy as np
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from math import isnan
from pprint import pprint as pp

"""
	portfolio_list structure:

	A list of position dictionary


	position dictionary strcture: (same as a row in the portfolio dataframe)

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


some other notes:
currenttime is a day number
days are numbered with integers with, day 0 = 1962-01-02

TODOS:
1. make a random portfolio generator. (input vector of days and bondtypes, returns a portfolio as defined in testing.py)
2. trim dataset to only include records where all bond types are availiable
3. start making time loop
4. consolidate helper functions
5. 



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

	offsetdates = (dates - float(currenttime))


	cdates = offsetdates[:-1]
	cpayments = payments[:-1]
	mdate = offsetdates[-1]
	mpayments = payments[-1]

	cdates, cpayments = zero_out(cdates, cpayments)

	presentvalue = position_value(position, currenttime)

	print "presentvalue"
	print presentvalue
	effrate = effective_rate(position = position)

	oneoverPV = 1/ presentvalue

	couponsum = np.sum((cdates/365) * cpayments / (effrate**cdates))

	finalsum = mdate/365 * mpayments/(effrate**mdate)

	macdur = oneoverPV* (couponsum + finalsum)


	return macdur


def mod_duration(position = None, currenttime = None):
	"""
	returns modified duration of a position at a currenttime
	"""

	macdur = mc_duration(position = position, currenttime = currenttime)
	effrate = effective_rate(position = position)

	moddur = macdur / effrate
	return moddur


def position_value(position = None, currenttime = None):
	"""
	calculate the value of a position, can accept long and short positions.
	but short positions have not been coded yet
	returns position value based on derivates market book.
	"""


	if position["positiontype"] == 'short':
		pass
		# do something

	if position["positiontype"] == 'long':
		"""
		
		"""
		# get effective rate and time period
		effrate = effective_rate(position = position)
		timeperiod = timeper(position = position)

		# get Payments and days
		Pc = position["couponpayments"] 
		tnow = position["coupondates"] - currenttime


		# set them relative to current time
		tnew, Pcnew = zero_out(tnow, Pc)

		posvalue = np.sum(Pcnew/(effrate**tnew))

	else:
		print "bad positiontype"
		return None

	return posvalue



def timeper(position = None):
	"""
	returns time period of bond, given a bondtype.
	This might not be used.
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
	daily effective rate for a bond, this also might be YTM
	"""

	# get interest rate and time period of possition
	interestrate = position["interestrate"]
	#timeperiod = timeper(position)

	effectiverate = (1 + interestrate)**(1./365)

	return effectiverate


def portfolio_duration(portfolio = None, Durationtype = 'mc', currenttime = None):
	"""
	returns either modified or macaulay duration for a portfolio
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

	# one day I will figure out how to deal with datetime objects. today is not that day though
	try:
		delta = datetimeobj - epoch
	except:
		delta = datetimeobj.to_datetime().date() - epoch

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


	newdate = epoch + datetime.timedelta(days = daynumber)

	return newdate


def todays_rates(daynumber = None, interestrate_df = None):
	"""
	grabs current days rates from interestrate_df
	"""

	# if no day number use todays number
	if daynumber == None:
		daynumber = date_to_day(date.today())

	# if no interestrate_df use fed dataset
	if not isinstance(interestrate_df, pd.DataFrame):
		interestrate_df = pd.read_csv("cleaned_data.csv")


	day_dict = interestrate_df.loc[[daynumber]].to_dict('records')[0]

	keys = day_dict.keys()


	# the following below is not nessicary if using the trimmed dataset.
	# remove day number and date for moment
	keys.remove('daynumber')
	keys.remove('date')

	clean_dict = {}

	# we only want bond types that have interest rates or exist.
	for key in keys:

		if isnan(day_dict[key]):
			pass

		else:
			clean_dict[key] = day_dict[key]



	clean_dict['daynumber'] = day_dict['daynumber']
	clean_dict['date'] = day_dict['date']

	return clean_dict


def zero_out(tnow = None, Pc = None):
	"""
	removes elements from tnow and Pc lists when tnow <= 0 
	"""

	tnew = []
	Pcnew = []
	k = 0
	for x in np.nditer(tnow):

		# if the day is less than zero do not add it.
	    if x >= 0:
	    	tnew.append(tnow[k])
	    	Pcnew.append(Pc[k])

	    k = k + 1

	tnew = np.array(tnew)
	Pcnew = np.array(Pcnew)

	return tnew, Pcnew


 
def pval(T,CF,Y,mode='disc'):
#   Computes present value of cash flows.
#    T    Term structure;  vector 1-by-N
#    CF   Cash flow;       vector 1-by-N
#    Y    Yield structure; vector 1-by-N
    if mode=='cont':
        s = CF/np.exp(Y*T)
        P = np.sum(s)
    elif mode=='disc':
        n = 365
        s = CF/((1+Y/n)**(n*T))
        P = np.sum(s)
    return P


 
class cBond:
    def new(self,faceValue,matMonths,annualCouponNum,couponRate,
            createDate = date(1962, 1, 2)):
    #   Constructs coupon bond at monthly scale. Assuming equally spaced 
    #    payments. Also assuming annualCouponNum is a factor of 12 and that 
    #    matMonths is a multiple of this factor.
    #
    #    faceValue         Face value of bond;  scalar
    #    matMonths         Months to maturity;   scalar
    #    annualCouponNum   Number of coupons per year;   scalar
    #    couponRate        Coupon value as a percent of face value;   scalar
    #    createDate        Date bond was created (i.e., day 0)
        if annualCouponNum == 0:
            C = np.array([faceValue])
            T = np.array([date_to_day(createDate+relativedelta(months=matMonths))])
        else:
            if 12 % annualCouponNum != 0:
                raise RuntimeError('annualCouponNum must be a factor of 12')    
            k = 12/annualCouponNum                             # step size (months)
            if matMonths % k != 0:
                raise RuntimeError('matMonths must align with annualCouponNum')
            n = matMonths/k                                    # number of payments
            cc = couponRate * faceValue       
            C = np.zeros(n)    
            T = np.zeros(n)
            for i in range(n):
                C[i] = cc;   
                T[i] = date_to_day(createDate+relativedelta(months=(i+1)*k))
                if i==n-1:
                    C[i] += faceValue 
        return C, T
    
'''
    def shift(self,bond,startMonth,endMonth):
    #   Shifts coupon bond for alignment with other bonds and timing.
    #
    #    bond          Bond object constructed by .new function
    #    startMonth    Month bond timing begins (prepending 0s)
    #    endMonth      Month bond tracking ends (postpending 0s)
        prepend = np.zeros((1,startMonth-1))
        sbond = np.append(prepend,bond)
        if endMonth > bond.size:
            postpend = np.zeros((1,endMonth-bond.size))
            sbond = np.append(sbond,postpend)
        return sbond
'''



									
