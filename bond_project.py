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

for x in np.arange(np.size(dates)):
    d = pd.Series(dates.format())
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

#%% Creating liabilities and computing transaction costs for Vasicek and normal
# rates


transaction_cost = 0.05 # 5% transaction costs - we can change this

for alpha in np.linspace(0.1, 1.00, num = 10):
    print alpha
    gamma = alpha
    Transaction = np.zeros(max_months)
    VTransaction = np.zeros(max_months)
    considered = 36

    LType = np.zeros(N)
    transaction = np.zeros(N)
    vtransaction = np.zeros(N)
    Vasicek = I.ix[considered:].copy()
    
    Vasicek.ix[0] = im.my_vasicek(I,considered)
    Vasicek.ix[0] = im.my_monthly_effective_rate(Vasicek.ix[0])
    
    # loop for FIRST MONTH ONLY in order to set liabilities
    for y in np.arange(N):
        if Type[y] == 1:
            continue
        pt = possible_types.copy()
        choice = pt[possible_types < Type[y]][-1]
        LType[y] = choice
        
        liability_interest = im.my_extract_rates(I,choice)
        LI = liability_interest[considered-1]
        LI = im.my_monthly_effective_rate(LI)
        li = np.random.uniform(0.01, 0.1)
        cr = coupon_rate[coupon_rate <= choice]
        ncp = cr[np.random.randint(np.size(cr))]
        Portfolio_L[y] = im.my_bond_generator(max_months, choice, 1, li, ncp)
        
        asset_rate = im.my_extract_rates(monthly_rates, Type[y])
        asset_rate = asset_rate[considered-1]
        
        macD_A = im.my_macD(Portfolio_A[y],asset_rate)
        macD_A = 12*macD_A
        macD_L = im.my_macD(Portfolio_L[y], LI)
        macD_L = 12*macD_L
        PVA = im.my_present_value(Portfolio_A[y], asset_rate)
        PVL = im.my_present_value(Portfolio_L[y], LI)
        
        Liability_number[y] = (macD_A*PVA/(1+asset_rate))/(macD_L*PVL/(1+LI))
        net = PVA - Liability_number[y]*PVL
        acquisition = Liability_number[y]*PVL
        
        transaction[y] = transaction_cost*(net + acquisition)
    
    VLiability_number = Liability_number.copy()
    Transaction[0] = np.sum(transaction)
    VTransaction[0] = np.sum(transaction)
    considered = considered +1
    
    # loop for ALL OTHER MONTHS
    for x in np.arange(1,max_months):
        np.delete(Portfolio_A, 0, axis = 1)
        np.delete(Portfolio_L, 0, axis = 1)
        new_Liability_number = np.zeros(N)
        new_VLiability_number = np.zeros(N)
        transaction = np.zeros(N)
        vtransaction = np.zeros(N)

        Vasicek.ix[x] = im.my_vasicek(I,considered)
        Vasicek.ix[x] = im.my_monthly_effective_rate(Vasicek.ix[x])
        
        ExpectedChange = np.zeros(N)
        VExpectedChange = np.zeros(N)
        
        # Find the maximum expected change in price based on data as well as
        # Vasicek estimate
        for y in np.arange(N):
            asset_rate = im.my_extract_rates(monthly_rates, Type[y])
            old_asset_rate = asset_rate[considered-2]
            asset_rate = asset_rate[considered-1]
            diff = np.abs(old_asset_rate - asset_rate)
            
            vasset_rate = im.my_extract_rates(Vasicek,Type[y])
            old_vasset_rate = vasset_rate[x-1]
            vasset_rate = vasset_rate[x]
            vdiff = np.abs(old_vasset_rate - vasset_rate)
            
            ExpectedChange[y] = diff*im.my_Price_Change(Portfolio_A[y],asset_rate, Coupons_per_year[y])
            VExpectedChange[y] = vdiff*im.my_Price_Change(Portfolio_A[y], vasset_rate, Coupons_per_year[y])
        
        maxChange = np.max(ExpectedChange)
        vmaxChange = np.max(VExpectedChange)
        
        # Calculate transaciton costs based on data
        for y in np.arange(N):
            if (gamma*maxChange >= ExpectedChange[y]):
                transaction[y] = 0
                continue
            else:
                if (Type[y] == 1):
                    transaction[y] = 0
                    continue
                liability_interest = im.my_extract_rates(I,LType[y])
                LI = liability_interest[considered-1]
                LI = im.my_monthly_effective_rate(LI)
                asset_rate = im.my_extract_rates(monthly_rates, Type[y])
                asset_rate = asset_rate[considered-1]
        
                macD_A = im.my_macD(Portfolio_A[y],asset_rate)
                macD_A = 12*macD_A
                macD_L = im.my_macD(Portfolio_L[y], LI)
                macD_L = 12*macD_L
                PVA = im.my_present_value(Portfolio_A[y], asset_rate)
                PVL = im.my_present_value(Portfolio_L[y], LI)
        
                new_Liability_number[y] = (macD_A*PVA/(1+asset_rate))/(macD_L*PVL/(1+LI))
                net = PVA - np.abs(new_Liability_number[y] - Liability_number[y])*PVL
                acquisition = np.abs(new_Liability_number[y] - Liability_number[y])*PVL
        
                transaction[y] = transaction_cost*(net + acquisition)
                Liability_number[y] = new_Liability_number[y]
        
        Transaction[x] = np.sum(transaction)
        
        # Calculate transaciton costs based on Vasicek estimate
        for y in np.arange(N):
            if (gamma*maxChange >= VExpectedChange[y]):
                vtransaction[y] = 0
                continue
            else:
                if (Type[y] == 1):
                    vtransaction[y] = 0
                    continue
                liability_interest = im.my_extract_rates(Vasicek,LType[y])
                LI = liability_interest[x]

                asset_rate = im.my_extract_rates(Vasicek, Type[y])
                asset_rate = asset_rate[x]
        
                macD_A = im.my_macD(Portfolio_A[y],asset_rate)
                macD_A = 12*macD_A
                macD_L = im.my_macD(Portfolio_L[y], LI)
                macD_L = 12*macD_L
                PVA = im.my_present_value(Portfolio_A[y], asset_rate)
                PVL = im.my_present_value(Portfolio_L[y], LI)
        
                new_VLiability_number[y] = (macD_A*PVA/(1+asset_rate))/(macD_L*PVL/(1+LI))
                net = PVA - np.abs(new_VLiability_number[y] - VLiability_number[y])*PVL
                acquisition = np.abs(new_VLiability_number[y] - VLiability_number[y])*PVL
        
                vtransaction[y] = transaction_cost*(net + acquisition)
                VLiability_number[y] = new_VLiability_number[y]
            
            VTransaction[x] = np.sum(vtransaction)
        considered = considered + 1








