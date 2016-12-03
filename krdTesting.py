import numpy as np
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta
import krdur as krd
import portfoliofuns as pf
import my_immunization as im

# TODO: Solve mismatched case


#%% [0] Load and prepare interest rate data.
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



#%% [00] Create a portfolio as in bond_project.py and extract one bond
possibleTypes = np.array([1.0, 3.0, 6.0, 12.0, 24.0, 36.0, 60.0, 84.0])
possibleCPY = np.array([1, 3, 4, 6, 12])

maxMonths = 84
numBonds = np.random.randint(20, 51)

L_portfolio = np.zeros((numBonds,maxMonths))
L_number = np.zeros(numBonds)
L_duration = np.zeros(numBonds)

[A_portfolio, Type, CPY] = im.my_portfolio_generator(numBonds,maxMonths)

bond = A_portfolio[0]
bond_type = Type[0]
bond_CPY = CPY[0]



#%% [1] Find present value and key rate duration of bond.
considered = 36
S0 = monthly_rates.ix[considered-1]                 # schedule at considered
U0 = [float(S0.index[i]) for i in range(S0.size)]   # extract terms
V0 = [float(S0.values[i]) for i in range(S0.size)]  # extract rates
X0 = np.arange(1,bond.size+1)                       # interpolated terms
Y0 = np.interp(X0,U0,V0)                            # interpolated rates

keybond0 = krd.krdbond(bond,Y0)

asset_rate = im.my_extract_rates(monthly_rates, Type[0])
asset_rate = asset_rate[considered-1] 
pval = im.my_present_value(bond,asset_rate)
macD = im.my_macD(bond,asset_rate)
  
print "Key rate durations (KRD):"      ;  print keybond0[0]
print "Present value (KRD): "          ;  print np.sum(keybond0[1])
print "Macaulay duration (my): "       ;  print macD
print "Modified duration (my): "       ;  print macD/(1+asset_rate)
print "Present value (my): "           ;  print pval               ;  print ' '


#%%  CAUTION YOU ARE ENTERING THE TWILIGHT ZONE CODE BELOW HAS NOT BEEN REVISED
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# [2] Test Case by Nathan
dt_str = '1/1/2016'
createDate = datetime.datetime.strptime(dt_str, "%m/%d/%Y").date()
CF6month, T6month = cbond.new(1000,6,6,.07,createDate)
Y6month = np.array([.046])
bond = { "interestrate" : Y6month,
         "createdate" : createDate,
         "coupondates" : T6month,
         "couponpayments" : CF6month} 
keybond6month = krd.krdbond(bond)

print "KRD of 6-month bond (2 month durations & full duration)"
print keybond6month[0]; print np.sum(keybond6month[0]); 
print "Present value: ";  print keybond6month[1];  print ' '

newtime = createDate + relativedelta(months=5)
keybond6monthnew = krd.krdbond(bond,currentTime=newtime)

print "KRD of 6-month bond (later date)"
print keybond6monthnew[0]; print np.sum(keybond6monthnew[0]); 
print "Present value: ";  print keybond6monthnew[1];  print ' '


#%%

# [3] Example from textbook
dt_str = '1/1/2012'
createDate = datetime.datetime.strptime(dt_str, "%m/%d/%Y").date()
CF, T = cbond.new(1000,5*12,1,.10,createDate)
T = [createDate + relativedelta(years=i+1) for i in range(5)]
Y = np.array([.05,.055,.0575,.059,.06])
bond = { "interestrate" : Y,
         "createdate" : createDate,
         "coupondates" : T,
         "couponpayments" : CF} 
keybond = krd.krdbond(bond,mode='cont')

print "KRD of 5-year bond (1 year durations & full duration)"
print keybond[0];  print np.sum(keybond[0]);
print "Present value: ";  print keybond[1];  print ' '


#%%

# [4] Portfolio construction and key rate duration
#      Based on Example 9.1 of Nawalkha et al. (2005)
dt_str = '1/1/2012'
createDate = datetime.datetime.strptime(dt_str, "%m/%d/%Y").date() 
   
bondConstructor = {
    "faceValues" : 1000*np.ones(5),
    "matMonths" : 12*np.arange(1,5+1,1),
    "annualCouponNum" : [1 for i in range(5)],
    "couponRate" : .10*np.ones(5),
    "createDate" : [createDate for i in range(5)],
    "interestrate" : [np.array([.05,.055,.0575,.059,.06]) for i in range(5)],
    "weight" : (1./5) * np.ones(5)                 }



def bonder(bC):
    # Creates a portfolio of bonds as specified by bond constructor bC.
    b = int(bC["weight"].size)
    L = ["interestrate","weight","createdate","coupondates","couponpayments"] 
    A = [ [bC["createDate"][i] for j in range(b-i-1)] for i in range(b) ]
    D = [cbond.new(bC["faceValues"][i],   # coupon dates
                    bC["matMonths"][i],
                    bC["annualCouponNum"][i],
                    bC["couponRate"][i],
                    bC["createDate"][i])[1] for i in range(b)]
    V = [bC["interestrate"],
         bC["weight"],
         [bC["createDate"][i] for i in range(b)],
         [ D[i] + A[i] for i in range(b)],
         [np.append(cbond.new(bC["faceValues"][i],   # coupon payments
                    bC["matMonths"][i],
                    bC["annualCouponNum"][i],
                    bC["couponRate"][i],
                    bC["createDate"][i])[0],np.zeros(b-i-1)) for i in range(b)]
          ]           
    portfolio = [{L[j]: V[j][i] for j in range(5)} for i in range(b) ]
    return portfolio

       
portfolio = bonder(bondConstructor)
portfolio_df = pd.DataFrame(portfolio)    

#newtime = pf.date_to_day(createDate + relativedelta(months=15))
newtime = createDate
keyport = krd.krdport(portfolio_df,newtime,mode='disc')

print "KRD of portfolio with 1-5 year bonds (1 year durations & full duration)"
print keyport[0];  print np.sum(keyport[0]); 
print "Present value: ";  print keyport[1]; print np.sum(keyport[1]);  print ' '

#%%

# [5] Instantaneous Returns
#     Shocking the yield curve
Yold = np.array([.05,.055,.0575,.059,.06])
Ynew = np.array([.055,.057,.0575,.058,.058])

def iret(T,CF,Yold,Ynew,mode):
    # Instantaneous return dP/P
    R = (pf.pval(T,CF,Ynew,mode) - pf.pval(T,CF,Yold,mode))/pf.pval(T,CF,Yold,mode)
    return R
    
T = np.array([[1, 0, 0, 0, 0],
              [1, 2, 0, 0, 0],
              [1, 2, 3, 0, 0],
              [1, 2, 3, 4, 0],
              [1, 2, 3, 4, 5]])
CF = np.array([[1100, 0, 0, 0, 0],
               [100, 1100, 0, 0, 0],
               [100, 100, 1100, 0, 0],
               [100, 100, 100, 1100, 0],
               [100, 100, 100, 100, 1100]])



def myinstantrun(T,CF,Yold,Ynew,mode):
    R = [];  D = np.append(T,CF,1)
    for d in D:
        R = np.append(R,iret(d[0:5],d[5:],Yold,Ynew,mode))
    return R
    
    
R = myinstantrun(T,CF,Yold,Ynew,'cont')
for r in R:
    print "Bond: {0:.3f}%".format(100*r)
    
    
# Weighting the bonds invested in...
ladder = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
barbell = np.array([0.479, 0, 0, 0, 0.521])
bullet = np.array([0, 0.521, 0, 0.479, 0])

portfolio_ladderR = np.sum(ladder*R)
print "Ladder: {0:.3f}%".format(100*portfolio_ladderR)

portfolio_barbellR = np.sum(barbell*R)
print "Barbell: {0:.3f}%".format(100*portfolio_barbellR)

portfolio_bulletR = np.sum(bullet*R)
print "Bullet: {0:.3f}%".format(100*portfolio_bulletR)


#%%

# [6] Key Rate Immunization (based on [4])
bond1 = portfolio[0];    bond2 = portfolio[1];    bond3 = portfolio[2]
bond4 = portfolio[3];    bond5 = portfolio[4];
bond6 = { "interestrate" : np.array([0.05, 0.055, 0.0575, 0.059, 0.06]),
         "createdate" : createDate,
         "coupondates" : [createDate, createDate, 
                          createDate, createDate,
                          createDate+relativedelta(years=5)],
         "couponpayments" : np.array([0, 0, 0, 0, 1000])} 

KRD1 = krd.krdbond(bond1,mode='cont')[0]
KRD2 = krd.krdbond(bond2,mode='cont')[0]
KRD3 = krd.krdbond(bond3,mode='cont')[0]
KRD4 = krd.krdbond(bond4,mode='cont')[0]
KRD5 = krd.krdbond(bond5,mode='cont')[0]
KRD6 = krd.krdbond(bond6,mode='cont')[0]

# Form KRD matrix
K = []
K = np.append(K,[KRD1, KRD2, KRD3, KRD4, KRD5, KRD6])
K = K.reshape(6,len(K)/6);  K = K.T
#K = np.concatenate((K,np.array([[1, 1, 1, 1, 1, 1]])),axis=0)

h = 4                                                # planning horizon (years)
DUR = np.array([0,0,0,4,0])
DUR = DUR.reshape(5,1)

# Solve for proportions of investments
# VERY BAD CONDITION NUMBER! Requires pseudo-inverse
# Unstable solution! Depends on day calculation, compounding, days per year...
p = np.linalg.lstsq(K,DUR)
r = np.linalg.matrix_rank(K)

print r

