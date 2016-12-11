# -*- coding: utf-8 -*-
"""
MATH 503 Project 2 Script
Authors: Anthony Gusman, Nathan Johnson, Nick Sullivan
"""

import pandas as pd
import numpy as np
import krdur as krd
import my_immunization as im
import portfoliofuns as pf
import bond_project_funs as bpf
from datetime import timedelta

#%% Generating a random portfolio over a planning horizon of 10 years

max_months = 84
N = 100 #np.random.randint(20, 51)
possible_types = np.array([1.0, 3.0, 6.0, 12.0, 24.0, 36.0, 60.0, 84.0])
K = np.array([1, 3, 6, 12, 24, 36, 60, 84])                    # set key rates
coupon_rate = np.array([1, 3, 4, 6, 12])
Portfolio_L = np.zeros((N,max_months))
Liability_number = np.zeros(N)
Duration_L = np.zeros(N)

[Portfolio_A, Type, Coupons_per_year] = im.my_portfolio_generator(N,max_months)

#%% Getting the monthly interest rate data

startdate = '3/1/2006'
enddate = '2/1/2016'
Data = pd.read_csv("trimmed_data.csv")
I = bpf.prepareData(Data,startdate,enddate)
monthly_rates = im.my_monthly_effective_rate(I)

#%% Creating liabilities and computing transaction costs for Vasicek and normal
# rates

transaction_cost = 0.05 # 5% transaction costs - we can change this

Transaction = np.zeros(max_months)
Transaction_krd = np.zeros(max_months)
VTransaction = np.zeros(max_months)
VTransaction_krd = np.zeros(max_months)
considered = 36        #use 3 years of prior data in interest calculations

LType = np.zeros(N)
transaction = np.zeros(N)
vtransaction = np.zeros(N)
Vasicek = I.ix[considered:].copy()
    
Vasicek.ix[0] = im.my_vasicek(I,considered)
Vasicek.ix[0] = im.my_monthly_effective_rate(Vasicek.ix[0])
    
# loop for FIRST MONTH ONLY in order to set liabilities
transaction, Liability_number, Portfolio_L, transaction_krd, Liability_number_krd, Portfolio_L_krd = bpf.firstMonth(N,Type,
               possible_types,considered,coupon_rate,max_months,
               monthly_rates,Portfolio_A,Portfolio_L,transaction_cost,I,
               LType,Liability_number,transaction,K)
    
VLiability_number = Liability_number.copy()
VLiability_number_krd = Liability_number_krd.copy()
Transaction[0] = np.sum(transaction)
Transaction_krd[0] = np.sum(transaction_krd)
VTransaction[0] = np.sum(transaction)
VTransaction_krd[0] = np.sum(transaction_krd)
considered = considered +1

FirstDF = pd.DataFrame(data = [np.zeros(max_months), np.zeros(max_months), np.zeros(max_months), np.zeros(max_months)],
                               index = ['Data Based', 'Vasicek Based','Data Based (krd)','Vasicek Based (krd)'])        
AlphaPanel = pd.Panel(data = {0.1 : FirstDF, 0.2 : FirstDF, 0.3 : FirstDF,
                              0.4 : FirstDF, 0.5 : FirstDF, 0.6 : FirstDF,
                              0.7 : FirstDF, 0.8 : FirstDF, 0.9 : FirstDF,
                              1.0 : FirstDF})
    
for alpha in np.linspace(0.1, 1.0, num = 10):
    considered = 37
    print alpha
    gamma = np.power(alpha,2)

    
    
    # loop for ALL OTHER MONTHS
    Transaction, VTransaction, Vasicek, Transaction_krd, VTransaction_krd = bpf.otherMonth(max_months,Portfolio_A,Portfolio_L,N,I,considered,Vasicek,
               monthly_rates,Type,Coupons_per_year,gamma,LType,
               Liability_number,transaction_cost,Transaction,
               VLiability_number,VTransaction,Liability_number_krd,
               Transaction_krd,Portfolio_L_krd,VTransaction_krd,
               VLiability_number_krd,K)   
    
    data = [Transaction, VTransaction, Transaction_krd, VTransaction_krd]
    print(data)
    index = ['Data Based','Vasicek Based','Data Based (krd)','Vasicek Based (krd)']
    TransactionDF = pd.DataFrame(data, index)
    InterestPanel = pd.Panel(data = {'Data Rates' :monthly_rates.ix[36:], 
                                     'Vasicek Rates' : Vasicek})
    AlphaPanel.ix[alpha] = TransactionDF
#    print(TransactionDF)
#    print(AlphaPanel)
#FOR ALPHA end


#%% Writing to CSV    
for x in np.linspace(0.1, 1.0, num = 10):
    df = AlphaPanel.ix[x]
    df.to_csv('pow2Gamma_Alpha=%s.csv' %x)

InterestPanel.ix['Data Rates'].to_csv('pow2Gamma_Data_Rates.csv')
InterestPanel.ix['Vasicek Rates'].to_csv('pow2Gamma_Vasicek_Rates.csv')