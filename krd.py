#####################
# KEY RATE DURATION #
#####################
#
# IMPORT PACKAGES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#
# DEFINITIONS
faceValue = 100
bondYears = 1
#
#                      We will assume that the coupon payouts are evenly spaced and equal 
couponNumberPerYear  = 4
#
#               This is the per coupon payout as a percentage of the face value
couponRate    = 0.10
#
#             Our convention is to express the terms in years.
curveTerms  = 1./12 * np.linspace(1,24,24)
#
#             Yields are in decimal form: 1.00% = 0.0100
curveYields = 1./100 * np.log10(1000 * np.linspace(1,24,24))
#
#           The key terms are assumed to be a subset of the yield curve terms.
keyTerms  = 1./12 * np.array([1,3,12,24])
#
#
bond = {"faceValue" : faceValue,
        "bondYears" : bondYears,
		"couponNumberPerYear" : couponNumberPerYear,
		"couponRate" : couponRate}
#
#		
yieldCurve = {"curveTerms" : curveTerms,
              "curveYields" : curveYields}
#
# BOND VALUE
def bondval(bond = None, yieldCurve = None):
	t   = bond["bondYears"]
	par = bond["faceValue"]
	m   = bond["couponNumberPerYear"]
	c   = bond["couponRate"] * par
	n   = m * t
	
	match = t==yieldCurve["curveTerms"]
	y     = yieldCurve["curveYields"][match]
	
	
	P_par    = par / (1+y/m)**n
	P_coupon = c / (1+y/m)**np.array([i+1 for i in range(np.int(n))])
	S = np.sum(P_coupon)
	P_bond = P_par + S
	return P_bond
#
# BOND VALUE DERIVATIVE
def partialbondval(bond = None, yieldCurve = None, keyTerms = None):
     t = keyTerms
     par = bond["faceValue"]
     m = bond["couponNumberPerYear"]
     c = bond["couponRate"] * par
     n = m * t
     
     y = np.zeros(np.size(n))
     S = np.zeros(np.size(n))
     for j in range(np.size(n)):  
         match = t[j]==yieldCurve["curveTerms"]
         y[j] = yieldCurve["curveYields"][match]
         S[j] = 0
         nj = np.int(n[j])
         for i in range(nj):
             S[j] = S[j] + (i+1)* (1./m) * c/(1+y[j]/m)**(i+1)

     P_par = (n/m) * par / (1+y/m)**n
             
     partials = -1/(1+y/m) * (P_par + S)
     return partials
#
# KEY RATE DURATION
def krdur(bond = None, yieldCurve = None, keyTerms = None):
    bondVals = np.zeros(np.size(keyTerms))
    for j in range(np.size(keyTerms)):
        bond["bondYears"] = keyTerms[j]
        bondVals[j] = bondval(bond = bond, yieldCurve = yieldCurve)
    partials = partialbondval(bond = bond, yieldCurve = yieldCurve, keyTerms = keyTerms)
    krd = -1./bondVals * partials
    return krd
    
krd = krdur(bond = bond, yieldCurve = yieldCurve, keyTerms = keyTerms)

'''
def krd(portfolio = None):
    terms = portfolio["terms"]
    yields = portfolio["yields"]
    krds = terms/(1 + yields)
    return krds
             
    
krds = krd(portfolio = portfolio)
duration = np.sum(krds)
#print krds, duration

newyields = 1./100 * np.array([3.65, 3.15, 3.38, 3.26, 3.03])
shifts = newyields - yields
newVal = 1 - np.sum(krds*shifts)
#print newVal


t = np.linspace(0,24,100)
def shift(t,terms,shifts):
    S = 0
    m = terms.size - 1
    for i in range(terms.size):       
        if i == 0:
            s = shifts[0]*(t<terms[0]) + shifts[0]*(terms[1]-t)/(terms[1]-terms[0])*(t>=terms[0])*(t<=terms[1]) + 0*(t>terms[1])
        elif i == m:
            s = 0*(t<terms[m-1]) + shifts[m]*(t-terms[m-1])/(terms[m]-terms[m-1])*(t>=terms[m-1])*(t<=terms[m]) + shifts[m]*(t>terms[m])
        else:
            s = shifts[i]*(t<terms[i-1]) + shifts[i]*(t-terms[i-1])/(terms[i]-terms[i-1])*(t>=terms[i-1])*(t<=terms[i]) + shifts[i]*(terms[i+1]-t)/(terms[i+1]-terms[i])*(t>=terms[i])*(t<=terms[i+1]) + 0*(t>terms[i+1])
        S = S + s
    return S

S = shift(t,12*terms,shifts)
print S

plt.plot(t,100*S,'k-')
plt.show()
'''

"""  
plt.plot(12*terms,100*yields,'k-s')
plt.plot(12*terms,100*newyields,'k-o')
plt.xlabel('months')
plt.ylabel('yields')
plt.show()
"""