import krdur as krd
import numpy as np

# NOTES:
#  .All computations performed assuming daily compounding (n = 365)
#  .All vectors and array elements are assumed to be encoded by the month
#    i.e., an interest rate vector Y = [.05,.06,.07] will be interpreted as
#    the 1-month, 2-month, and 3-month interest rates
#  .KRD compuatations require 'annualized' effective rates in current testing
#  .KRD computations require monthly term vector to be converted in terms of
#    years; e.g., T = [1,2] months    must be inputted as 
#    T = (1./12)*[1,2] years; this is likely a consequence of using annualized
#    interest rates
#  .Portfolio computations currently performed on class object BONDS
#  .Cash flow objects are Numpy arrays produced by class krd.cBond()


# Coupon bond class object
cb = krd.cBond()


# [1] Single bond present value and key rate durations
T0 = (1./12)*np.arange(1,60+1,1)
Y0 = np.array([0,0,0,0,0,0,0,0,0,0,0,.05,
               0,0,0,0,0,0,0,0,0,0,0,.055,
               0,0,0,0,0,0,0,0,0,0,0,.0575,
               0,0,0,0,0,0,0,0,0,0,0,.059,
               0,0,0,0,0,0,0,0,0,0,0,.06])
CF0 = cb.new(1000,12,1,.10);  CF0 = cb.shift(CF0,1,60)
p = krd.pvalcf(T0,CF0,Y0)
keybond0 = krd.krdbond(T0,CF0,Y0)



# [2] Test Case by Nathan
def exxP(effY,n):
    # !! KRD computation requires annualized effective rates.
    py = n*((1+effY)**(1./n) - 1)
    return py

ym = exxP(.046,365)   # sample annualized exact rate
    
T6month = (1./12)*np.array([1,2,3,4,5,6])
Y6month = ym*np.ones((1,6))
CF6month = cb.new(1000,6,6,.07)
keybond6month = krd.krdbond(T6month,CF6month,Y6month)



# [3] Example from textbook
T = (1./12)*np.arange(1,60+1,1)
Y = np.array([0,0,0,0,0,0,0,0,0,0,0,.05,
              0,0,0,0,0,0,0,0,0,0,0,.055,
              0,0,0,0,0,0,0,0,0,0,0,.0575,
              0,0,0,0,0,0,0,0,0,0,0,.059,
              0,0,0,0,0,0,0,0,0,0,0,.06])
CF = cb.new(1000,60,1,0.1)
keybond = krd.krdbond(T,CF,Y)



# [4] Portfolio construction and key rate duration
#      Based on Example 9.1 of Nawalkha et al. (2005)
Bond1 = cb.new(1000,12,1,.10);  Bond1 = cb.shift(Bond1,1,60)
Bond2 = cb.new(1000,24,1,.10);  Bond2 = cb.shift(Bond2,1,60)
Bond3 = cb.new(1000,36,1,.10);  Bond3 = cb.shift(Bond3,1,60)
Bond4 = cb.new(1000,48,1,.10);  Bond4 = cb.shift(Bond4,1,60)
Bond5 = cb.new(1000,60,1,.10);  Bond5 = cb.shift(Bond5,1,60)
    
class BONDS:
    T = (1./12)*np.arange(1,60+1,1)
    Y = np.array([0,0,0,0,0,0,0,0,0,0,0,.05,
                  0,0,0,0,0,0,0,0,0,0,0,.055,
                  0,0,0,0,0,0,0,0,0,0,0,.0575,
                  0,0,0,0,0,0,0,0,0,0,0,.059,
                  0,0,0,0,0,0,0,0,0,0,0,.06])
    CF = np.array([Bond1,Bond2,Bond3,Bond4,Bond5])       

W = np.array([0.2,0.2,0.2,0.2,0.2])

keyport = krd.krdport(W,BONDS)