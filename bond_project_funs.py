"""
BOND PROJECT FUNCTIONS
   Various functions required by bond_project.py script.

9 December 2016
Authors: Anthony Gusman, Nathan Johnson, Nick Sullivan
"""

import pandas as pd
import numpy as np
from datetime import timedelta

import my_immunization as im
import portfoliofuns as pf


###############################PREPARING DATA##################################
def prepareData(Data,startdate,enddate):
    Data = Data.as_matrix()
    Data = Data[148:, 2:11]
    Data = pd.DataFrame(Data[:,1:], index = Data[:,0], columns = ['1.0', '3.0', '6.0', '12.0', '24.0', '36.0', '60.0', '84.0'])
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
    return I



#################################FIRST MONTH###################################   
def firstMonth(N,Type,possible_types,considered,coupon_rate,max_months,
               monthly_rates,Portfolio_A,Portfolio_L,transaction_cost,I,
               LType,Liability_number,transaction):
# Inputs: N, possible_types, Type, I, considered, coupon_rate, max_months,
#         monthly_rates, Portfolio_A, Portfolio_L, Liability_number   
    for y in np.arange(N):
        if Type[y] == 1:
            continue
        pt = possible_types.copy()
        choice = pt[possible_types <= Type[y]][-1]
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
    return transaction, Liability_number, Portfolio_L
    
#################################OTHER MONTHS##################################
def otherMonth(max_months,Portfolio_A,Portfolio_L,N,I,considered,Vasicek,
               monthly_rates,Type,Coupons_per_year,gamma,LType,
               Liability_number,transaction_cost,Transaction,
               VLiability_number,VTransaction):
    # loop for ALL OTHER MONTHS
    for x in np.arange(1,max_months):
        newPortfolio_A = np.delete(Portfolio_A, np.arange(x-1), axis = 1)
        newPortfolio_L = np.delete(Portfolio_L, np.arange(x-1), axis = 1)
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
            diff = np.absolute(old_asset_rate - asset_rate)
            
            vasset_rate = im.my_extract_rates(Vasicek,Type[y])
            old_vasset_rate = vasset_rate[x-1]
            vasset_rate = vasset_rate[x]
            vdiff = np.absolute(old_vasset_rate - vasset_rate)
            
            ExpectedChange[y] = diff*im.my_Price_Change(newPortfolio_A[y],asset_rate, Coupons_per_year[y])
            VExpectedChange[y] = vdiff*im.my_Price_Change(newPortfolio_A[y], vasset_rate, Coupons_per_year[y])
        #FOR expected end     
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
                
                PVA = im.my_present_value(newPortfolio_A[y], asset_rate)
                PVL = im.my_present_value(newPortfolio_L[y], LI)
                
                if (PVA == 0):
                    transaction[y] = 0
                    continue
        
                macD_A = im.my_macD(newPortfolio_A[y],asset_rate)
                macD_A = 12*macD_A
                macD_L = im.my_macD(newPortfolio_L[y], LI)
                macD_L = 12*macD_L
                if (macD_L == 0):
                    transaction[y] = 0
                    continue
        
                new_Liability_number[y] = (macD_A*PVA/(1+asset_rate))/(macD_L*PVL/(1+LI))
                net = PVA - np.abs(new_Liability_number[y] - Liability_number[y])*PVL
                acquisition = np.abs(new_Liability_number[y] - Liability_number[y])*PVL
        
                transaction[y] = transaction_cost*(net + acquisition)
                Liability_number[y] = new_Liability_number[y]
        #FOR transaction end        
        Transaction[x] = np.sum(transaction)
        
        # Calculate transaciton costs based on Vasicek estimate
        for y in np.arange(N):
            if (gamma*vmaxChange >= VExpectedChange[y]):
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
                
                PVA = im.my_present_value(newPortfolio_A[y], asset_rate)
                PVL = im.my_present_value(newPortfolio_L[y], LI)
                
                if (PVA == 0):
                    vtransaction[y] = 0
                    continue
        
                macD_A = im.my_macD(newPortfolio_A[y],asset_rate)
                macD_A = 12*macD_A
                macD_L = im.my_macD(newPortfolio_L[y], LI)
                macD_L = 12*macD_L
                
                if (macD_L == 0):
                    vtransaction[y] = 0
                    continue
                
                new_VLiability_number[y] = (macD_A*PVA/(1+asset_rate))/(macD_L*PVL/(1+LI))
                net = PVA - np.abs(new_VLiability_number[y] - VLiability_number[y])*PVL
                acquisition = np.abs(new_VLiability_number[y] - VLiability_number[y])*PVL
        
                vtransaction[y] = transaction_cost*(net + acquisition)
                VLiability_number[y] = new_VLiability_number[y]
        #FOR vtransaction end
        VTransaction[x] = np.sum(vtransaction)            
        considered = considered + 1
    #FOR x end        
    return Transaction, VTransaction, Vasicek
'''
# loop for ALL OTHER MONTHS
    for x in np.arange(1,max_months):
        newPortfolio_A = np.delete(Portfolio_A, np.arange(x-1), axis = 1)
        newPortfolio_L = np.delete(Portfolio_L, np.arange(x-1), axis = 1)
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
            diff = np.absolute(old_asset_rate - asset_rate)
            
            vasset_rate = im.my_extract_rates(Vasicek,Type[y])
            old_vasset_rate = vasset_rate[x-1]
            vasset_rate = vasset_rate[x]
            vdiff = np.absolute(old_vasset_rate - vasset_rate)
            
            ExpectedChange[y] = diff*im.my_Price_Change(newPortfolio_A[y],asset_rate, Coupons_per_year[y])
            VExpectedChange[y] = vdiff*im.my_Price_Change(newPortfolio_A[y], vasset_rate, Coupons_per_year[y])
'''    
    
    
    
    
    
    
    
#############################GENERATE PORTFOLIO################################
'''
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
'''