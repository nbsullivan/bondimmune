import numpy as np
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import krdur as krd
import portfoliofuns as pf


# TODO: Solve mismatched case


# Coupon bond class object
cbond = pf.cBond()


# [1] Single 1-coupon bond present value and key rate durations
dt_str = '1/1/2012'
createDate = datetime.datetime.strptime(dt_str, "%m/%d/%Y").date()
CF0, T0 = cbond.new(100,3,0,.10,createDate)
Y0 = np.array([.06])
bond = { "interestrate" : Y0,
         "createdate" : pf.date_to_day(createDate),
         "coupondates" : T0,
         "couponpayments" : CF0} 
keybond0 = krd.krdbond(bond)
  
print "KRD of 0-coupon bond";  print np.sum(keybond0[0]); 
print "Present value: ";  print np.sum(keybond0[1]);  print ' '


#%%

# [2] Test Case by Nathan
dt_str = '1/1/2016'
createDate = datetime.datetime.strptime(dt_str, "%m/%d/%Y").date()
CF6month, T6month = cbond.new(1000,6,6,.07,createDate)
Y6month = np.array([.046])
bond = { "interestrate" : Y6month,
         "createdate" : pf.date_to_day(createDate),
         "coupondates" : T6month,
         "couponpayments" : CF6month} 
keybond6month = krd.krdbond(bond)

print "KRD of 6-month bond (2 month durations & full duration)"
print keybond6month[0]; print np.sum(keybond6month[0]); 
print "Present value: ";  print keybond6month[1];  print ' '

newtime = pf.date_to_day(createDate + relativedelta(months=5))
keybond6monthnew = krd.krdbond(bond,currentTime=newtime)

print "KRD of 6-month bond (later date)"
print keybond6monthnew[0]; print np.sum(keybond6monthnew[0]); 
print "Present value: ";  print keybond6monthnew[1];  print ' '


#%%

# [3] Example from textbook
dt_str = '1/1/2012'
createDate = datetime.datetime.strptime(dt_str, "%m/%d/%Y").date()
CF, T = cbond.new(1000,5*12,1,.10,createDate)
T = pf.date_to_day(createDate) + 365*np.arange(1,5+1,1) # ignore leap years
Y = np.array([.05,.055,.0575,.059,.06])
bond = { "interestrate" : Y,
         "createdate" : pf.date_to_day(createDate),
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
    V = [bC["interestrate"],
         bC["weight"],
         [pf.date_to_day(bC["createDate"][i]) for i in range(b)],
         [np.append(cbond.new(bC["faceValues"][i],   # coupon dates
                    bC["matMonths"][i],
                    bC["annualCouponNum"][i],
                    bC["couponRate"][i],
                    bC["createDate"][i])[1],
                    pf.date_to_day(bC["createDate"][i])*np.ones(b-i-1)) for i in range(b)],
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

newtime = pf.date_to_day(createDate + relativedelta(months=15))
#newtime = pf.date_to_day(createDate)
keyport = krd.krdport(portfolio_df,newtime)

print "KRD of portfolio with 1-5 year bonds (1 year durations & full duration)"
print keyport[0];  print np.sum(keyport[0]); 
print "Present value: ";  print keyport[1]; print np.sum(keyport[1]);  print ' '


