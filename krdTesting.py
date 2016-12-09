# KEY RATE DURATION TUTORIAL
#    Calculate key rate durations of individual bonds and/or portfolios.
#
# 8 December 2016
# Anthony Gusman, Nathan Johnson, Nick Sullivan
#
# References:
#    Nawalkha, Soto, and Beliaeva. 2005. Interest Rate Risk Modeling: The 
#       Fixed Income Valuation Course. John Wiley & Sons, Inc. New Jersey.



import numpy as np                               # MATLAB-style functions
import scipy as sp
import pandas as pd                              # Dataframe functions
from scipy import optimize
from datetime import timedelta


import krdur as krd                              # Key rate duration
import my_immunization as im                     





#%% [0] Loading and preparing interest rate data...
startdate = '3/1/2006'
enddate = '2/1/2016'
Data = pd.read_csv("trimmed_data.csv")     # treasury maturity rates over time


# Preprocessing...
Data = Data.as_matrix()                       # ...removes row IDs and headers
Data = Data[:, 2:11]                      # cut 'Unnamed' and 'daynumber' cols


# Create 'I': Filtered dataframe by business days; restricted to date interval                                        
Data = pd.DataFrame(Data[:,1:], index = Data[:,0], columns = ['1.0', '3.0', '6.0',
                    '12.0', '24.0', '36.0', '60.0', '84.0'])
dates = pd.date_range(startdate, enddate, freq = 'BMS')  # business day filter
date_strs = pd.Series(dates.format())
I = Data.ix[date_strs]


# Cleaning data...
for x in range(dates.size):
    rate1 = I.ix[date_strs.ix[x]].ix[0];
    if np.isnan(rate1):
        new_date =  dates[x] + timedelta(1)
        new_index = pd.date_range(new_date, new_date)
        new_string = pd.Series(new_index.format())[0]

        # Special cases
        if (new_string == '2010-01-02'):
            new_string = '2010-01-04'
        if (new_string == '2016-01-02'):
            new_string = '2016-01-04'

        I.ix[date_strs.ix[x]] = Data.ix[new_string]    # replace with new data
        I.T.columns.values[x] = new_string             # rename accordingly


# Converting: annual percent >> annual decimal >> monthly decimal  
I = I/100
M = im.my_monthly_effective_rate(I)



#%% [1] Creating a portfolio and extracting a bond...

# Setting global maturity lengths (Types) and coupons per year (CPY)...
possibleTypes = np.array([1.0, 3.0, 6.0, 12.0, 24.0, 36.0, 60.0, 84.0])
possibleCPY = np.array([1, 3, 4, 6, 12])     


# Building an asset portfolio...            
maxMonths = 84                                       # longest maturity length
numBonds = np.random.randint(20, 51)            # number of bonds in portfolio
PORT = im.my_portfolio_generator(numBonds, maxMonths)
[PORT_assets, PORT_types, PORT_CPYs] = [PORT[0], PORT[1], PORT[2]]


# Extracing a particular bond...
bondID = 0;
bond_CF   = PORT_assets[bondID]
bond_type = PORT_types[bondID]
bond_CPY  = PORT_CPYs[bondID]




# 
L_portfolio = np.zeros((numBonds,maxMonths))
L_number = np.zeros(numBonds)
L_duration = np.zeros(numBonds)



#%% [2] Interpolating interest rates for key rate duration calculations...
windowSize = 36
S = M.ix[windowSize-1]                             # current schedule
U = [float(S.index[i]) for i in range(S.size)]   # extract terms
V = [float(S.values[i]) for i in range(S.size)]  # extract rates
X = np.arange(maxMonths)+1                         # interpolated terms
Y = np.interp(X,U,V)                            # interpolated rates







#%% [3] Finding present value and key rate duration of bond...
K = np.array([1, 3, 6, 12, 24, 36, 60, 84])                    # set key rates
bond_KRD,bond_PV = krd.bond(bond_CF,Y,K)

print "Key rate durations (KRD):"      ;  print bond_KRD
print "Sum of krd: "                   ;  print np.sum(bond_KRD)
print "Present value (KRD): "          ;  print bond_PV


# Difference compared to standard valuation...
asset_rate = im.my_extract_rates(M, bond_type)
asset_rate = asset_rate[windowSize-1] 
pval = im.my_present_value(bond_CF,asset_rate)
macD = im.my_macD(bond_CF,asset_rate)
  
print "Macaulay duration (my): "       ;  print macD
print "Modified duration (my): "       ;  print macD/(1+asset_rate)
print "Present value (my): "           ;  print pval               ;  print ' '



#%% [4] Finding present value and key rate duration of portfolio...
Q = np.ones(numBonds)
PORT_KRD,PORT_PV = krd.portfolio(PORT_assets,Y,Q,K)




#%% [5] Creating liability types for KRD solution...
NL = K.size + 1;                               # same number as key rate durations
maturities = np.array([1, 3, 6, 12, 24, 36, 60, 84])
coupon_rate = np.array([1, 3, 4, 6, 12])


def Lgen(N,max_months,possible_duration,coupon_rate):
    Coupons_per_year = np.zeros(N)
    Interest = np.zeros(N)
    Pl = np.zeros((N,max_months))
    r = np.arange(N)
    Typel = np.zeros(N)
    
    for x in r:
        i = np.random.uniform(0.01, 0.1)
        Interest[x] = i
        possible_duration = possible_duration[possible_duration <= max_months]
        tipe = possible_duration[x]
        Typel[x] = tipe
        cr = coupon_rate[coupon_rate <= tipe]
        ncp = cr[np.random.randint(np.size(cr))] # calculate the number of
                                                 # coupon payments in a year
        Coupons_per_year[x] = ncp
        Pl[x] = im.my_bond_generator(max_months, tipe, 1, i, ncp)
    
    
        L_portfolio = Pl
        L_Type = Typel
        L_CPY = Coupons_per_year
    return L_portfolio, L_Type, L_CPY

[LPORT_CF, LPORT_types, LPORT_CPYs] = Lgen(NL,maxMonths,maturities,coupon_rate)



#%% [6] Finding immunized position...

# immunize(Pa,Y,Qa,Pl,K,w0='null',r=0.5):
Qa = np.ones(krd.nbonds(PORT_assets))
N_liabilitiesToShort,err = krd.immunize(PORT_assets,Y,Qa,LPORT_CF,K)

print 'Recommended short amounts: ';   print np.negative(N_liabilitiesToShort)






