import pandas as pd
import numpy as np
import my_immunization as im
import portfoliofuns as pf
from datetime import timedelta

#%%
def my_bond_generator(max_months, month_duration, face_value, coupon_rate, ncp):
    
    """
    my_bond_generator is a function that will create a row vector
    of payments based on the following arguments:
    
        max_months - the maximum number of months in the entire portfolio
                     (i.e., our planning horizon).
        month_duration - the number of months for which the created bond will 
                         make payments.
        face_value - the face or par value of the bond.
        coupon_rate - the percentage of the face value that will be used
                      as the coupon payment amount (5% = 0.05).
        ncp      -    the Number of Coupon Payments in a year (used to pad 0's)
                      and must be a factor of 12.
    
    The created vector will be a list of MONTHLY payments (if no payment at
    a particular month, then the value will be 0 in that element) and the size
    of the vector will be equal to max_months.  Thus, the first element of 
    the created vector will be the payment at month 1.
    
    EXAMPLE: To create a 6-month bond with bi-monthly coupon payments at 5%,
             and a par value of $100, we would call
             
             B = my_bond_generator(max_months, 6, 100, 0.05, 6),
             
             where max_months would depend on our portfolio makeup.
             
    """
    
    B = np.zeros(max_months)
    cp = face_value*coupon_rate
    
    if (12%ncp != 0):
        raise RuntimeError('number of coupons in a year must be a factor of 12')

    step_size = 12/ncp
    B[step_size - 1:month_duration - 1:step_size] = cp
    B[month_duration - 1] = (1+coupon_rate)*face_value
    
    return B

#%%
def my_Price_Change(B, i, ncp):
    
    """
    my_Price_Change will compute the expected change in price per UNIT change
    in the interest rate using the following arguments:
    
        B - a row vector of bond payments (from my_bond_generator)
        i - the interest rate at which the bond was purchased
        ncp - the number of coupon payments in a year for bond B
    
    The output will be a single number.  To convert the ouput to actual changes
    in interest rate, you must multiply the output by the percentage change
    in the rate to a unit.
    
    EXAMPLE: P = my_Price_Change(B,0.1,12) will give the price change for a
             bond, B, created through the function my_bond_generator that pays
             monthly coupons.  Suppose the interest rate changes from 10% to 
             10.1%.  We would multiply Price_Change by (10.1-10)/1 = 0.1 to 
             find the actual change in bond price.
             
    """
    
    ncp = float(ncp)
    s = np.size(B)
    Range = np.arange(1,s+1)
    Discount = 1/((1+i)**Range)
    Change = Discount*B*(Range/ncp)
    Price_Change = np.sum(Change)
    Price_Change = Price_Change/(1+i)
    return -Price_Change
 
#%%
def my_portfolio_generator(N, max_months):
    possible_duration = np.array([1, 3, 6, 12, 24, 36, 60, 84])
    coupon_rate = np.array([1, 3, 4, 6, 12])
    Coupons_per_year = np.zeros(N)
    Interest = np.zeros(N)
    P = np.zeros((N,max_months))
    r = np.arange(N)
    Type = np.zeros(N)
    
    for x in r:
        i = np.random.uniform(0.01, 0.1)
        Interest[x] = i
        possible_duration = possible_duration[possible_duration <= max_months]
        tipe = possible_duration[np.random.randint(np.size(possible_duration))]
        Type[x] = tipe
        cr = coupon_rate[coupon_rate <= tipe]
        ncp = cr[np.random.randint(np.size(cr))] # calculate the number of
                                                 # coupon payments in a year
        Coupons_per_year[x] = ncp
        P[x] = im.my_bond_generator(max_months, tipe, 1, i, ncp)
    
    return P, Type, Coupons_per_year

#%%
def my_extract_rates(I, Type):
    return I.T.ix[str(Type)]
#%%
def my_monthly_effective_rate(I):
    I = (1+I)**(1.0/12) - 1
    return I

#%%
def my_present_value(B, i):
    s = np.size(B)
    t = np.arange(s)+1
    PV = np.sum(B/((1+i)**t))
    return PV

#%%
def my_macD(B, i):
    PV = im.my_present_value(B,i)
    s = np.size(B)
    t = np.arange(s)+1
    Discount = (1+i)**(-t)
    factors = B*Discount
    macD = (1/PV)*np.sum((t/12.0)*factors)
    return macD

#%%

def my_vasicek(I, considered):
    Considered_I = I.ix[:considered]
    DeltaT = 1
    n = considered
    A = np.zeros(8)
    B = np.zeros(8)
    sigma = np.zeros(8)
    Anticipated = np.zeros(8)
    
    for x in np.arange(8):
        ratek = Considered_I.T.ix[x][0:n-1]
        ratekplusone = Considered_I.T.ix[x][1:]
        B[x] = (np.sum(ratek*ratekplusone) - np.sum(ratek)*
                np.sum(ratekplusone)/n)/(np.sum(ratek*ratek) - np.sum(ratek)*
                np.sum(ratek)/n)
        A[x] = np.sum(ratekplusone)/n-B[x]*np.sum(ratek)/n
        sigma[x] = np.sqrt(np.sum((ratekplusone-B[x]*ratek - A[x])**2)/n)
        Anticipated[x] = ratekplusone[n-2] + (A[x]/B[x]) + sigma[x]*np.random.normal(0,DeltaT)
    return Anticipated