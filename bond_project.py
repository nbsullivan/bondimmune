# -*- coding: utf-8 -*-
"""
MATH 503 Project 2 Script
Authors: Anthony Gusman, Nathan Johnson, Nick Sullivan
"""

import pandas as pd
import numpy as np
import my_immunization as im
import portfoliofuns as pf
from datetime import timedelta

#%% Generating a random portfolio over a planning horizon of 10 years

max_months = 84
N = np.random.randint(20, 51)
possible_types = np.array([1.0, 3.0, 6.0, 12.0, 24.0, 36.0, 60.0, 84.0])
coupon_rate = np.array([1, 3, 4, 6, 12])
Portfolio_L = np.zeros((N,max_months))
Liability_number = np.zeros(N)
Duration_L = np.zeros(N)

[Portfolio_A, Type, Coupons_per_year] = im.my_portfolio_generator(N,max_months)


#%% Getting the monthly interest rate data

startdate = '3/1/2006'
enddate = '2/1/2016'
Data = pd.read_csv("trimmed_data.csv")
Data = Data.as_matrix()
Data = Data[148:, 2:11]
Data = pd.DataFrame(Data[:,1:], index = Data[:,0], columns = ['1.0', '3.0', '6.0',
                    '12.0', '24.0', '36.0', '60.0', '84.0'])
dates = pd.date_range(startdate, enddate, freq = 'BMS')
date_strings = pd.Series(dates.format())
I = Data.ix[date_strings]


# generating list of dates at beigings of months, cleans NaNs
for x in np.arange(np.size(dates)):

    d = pd.Series(dates.format())      # (!) inefficient declare outside loop
    if np.isnan(I.ix[d.ix[x]].ix[0]):
        new_index = pd.date_range(dates[x] + timedelta(1), dates[x] + timedelta(1))
        new_string = pd.Series(new_index.format())
        new_string = new_string[0]
        if (new_string == '2010-01-02'):
            new_string = '2010-01-04'
        if (new_string == '2016-01-02'):
            new_string = '2016-01-04'

        I.ix[d.ix[x]] = Data.ix[new_string]
        I.T.columns.values[x] = new_string
     
I = I/100
monthly_rates = im.my_monthly_effective_rate(I)

#%% Creating liabilities and computing transaction costs for FIRST MONTH ONLY

# alpha risk tolarance
alpha = 0.5

# sorta randomized transaction costs
transaction_cost = np.random.uniform(0.01, 0.05)

print 'Transaction Percentage: ', 100*transaction_cost, '%'

# gamma something to do with risk tolarance
gamma = np.exp(alpha - 1)
Transaction = np.zeros(max_months)           # cost of portfolio over all time

# number of months worth of data to use for vasicek model
considered = 36

# begiing of the major loop only working for the first month

for x in np.array([0]):


    transaction = np.zeros(N)               # cost of portfolio for this month
    for y in np.arange(N):
        if Type[y] == 1:             # if bond expires in one month, ignore it
            continue
        pt = possible_types.copy()
        choice = pt[possible_types < Type[y]][-1]   # liability bond will be one less type than asset
        
        # generating libaiblilty portfolio
        liability_interest = im.my_extract_rates(I,choice)  # extract historical annual interest rate over all time for liability type
        LI = liability_interest[considered-1]    # pick the last known interest rate within the interval [startdate,startdate+considered]
        LI = im.my_monthly_effective_rate(LI)    # convert to monthly
        li = np.random.uniform(0.01, 0.1)        # random coupon percent value
        cr = coupon_rate[coupon_rate <= choice]  # possible coupon per year schedules
        ncp = cr[np.random.randint(np.size(cr))] # pick one of them
        Portfolio_L[y] = im.my_bond_generator(max_months, choice, 1, li, ncp)
        
        asset_rate = im.my_extract_rates(monthly_rates, Type[y])  # extract historical monthly interest rate over all time for asset type
        asset_rate = asset_rate[considered-1]    # pick the last known interest rate within the interval [startdate,startdate+considered]
        
        # getting durations for each position, assests and liabilities
        macD_A = im.my_macD(Portfolio_A[y],asset_rate)   # duration in years
        macD_A = 12*macD_A                               # duration in months
        macD_L = im.my_macD(Portfolio_L[y], LI)          # duration in years
        macD_L = 12*macD_L                               # duration in months

        # present values
        PVA = im.my_present_value(Portfolio_A[y], asset_rate)
        PVL = im.my_present_value(Portfolio_L[y], LI)

        # computing N as a vector which will be over written
        Liability_number[y] = (macD_A*PVA/(1+asset_rate))/(macD_L*PVL/(1+LI))

        # see macdonalds book, net is generating a tranasction cost
        net = PVA - Liability_number[y]*PVL

        # aqquring libabilites generates transaction costs
        acquisition = Liability_number[y]*PVL    # (!) inefficient, compute prior to net
        
        # cost associated with yth bond 
        transaction[y] = transaction_cost*(net + acquisition)
    # total transaction cost for porfolio at Xth month.
    Transaction[x] = np.sum(transaction)

print Transaction
        
        
        
        
        









