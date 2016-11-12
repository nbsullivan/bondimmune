# KEY RATE DURATION FUNCTIONS
#    Calculate key rate durations of individual bonds and/or portfolios
#     assuming yields are zero-coupon rates compounded continuously.
#
# 12 November 2016
# Anthony Gusman
#
# References:
#    Nawalkha, Soto, and Beliaeva. 2005. Interest Rate Risk Modeling: The 
#       Fixed Income Valuation Course. John Wiley & Sons, Inc. New Jersey.



import numpy as np                               # MATLAB-style functions



def krdbond(T,CF,Y):
#   Computes key rate durations of cash flows. Assuming continuous compounding.
#    T    Term structure;  vector 1-by-N
#    CF   Cash flow;       vector 1-by-N
#    Y    Yield structure; vector 1-by-N    
    P = pvalcf(T,CF,Y)
    KRD = 1/P * CF*T/np.exp(Y*T)
    return KRD

    
     
def pvalcf(T,CF,Y,mode='cont'):
#   Computes present value of cash flows. Assuming continuous compounding.
#    T    Term structure;  vector 1-by-N
#    CF   Cash flow;       vector 1-by-N
#    Y    Yield structure; vector 1-by-N
    if mode=='cont':
        s = CF/np.exp(Y*T)
        P = np.sum(s)
    return P
#######################################1#######################################


def krdport(W,BONDS):
#   Computes key rate duration of portfolio.
#    W       Weighting strategy;  vector 1-by-N
#    BONDS   Class object consisting of:
#       ~.T    Term structure;   vector 1-by-N
#       ~.Y    Yield structure;  vector 1-by-N
#       ~.CF   Cash flow array (row-by-row);  array B-by-N
    b = BONDS.CF.shape[0]
    if W.size != b:
        raise RuntimeError("Dimension mismatch! Weights, number of bonds unequal!")
    T = BONDS.T;     m = T.size;   Y = BONDS.Y

    KRD = np.zeros((b,m))
    for i in range(b):
        KRD[i] = krdbond(T,BONDS.CF[i],Y)
    
    S = W*np.transpose(KRD)
    KRDport = np.sum(S,1)
    return KRDport
    
    
    
def cBond(faceValue,matYears,annualCouponNum,couponRate,offset=0,fillTill=None,):
#   Constructs coupon bond.
#    faceValue         Face value of bond;  scalar
#    matYears          Years to maturity;   scalar
#    annualCouponNum   Number of coupons per year;   scalar
#    couponRate        Coupon value as a percent of face value;   scalar
#
#    OPTIONAL: These are usually used to align bonds for portfolios.
#    offset            periods to prefill with zeros
#    fillTill          periods to postfill with zeros
    L = np.round(matYears*annualCouponNum)
    if fillTill==None:
        L0 = L
    else:
        L0 = np.round(fillTill)
    cc = couponRate * faceValue
    C = np.zeros((1,L0))
    for i in np.arange(offset,offset+L):
        C[0,i] = cc
        if i==L-1:
            C[0,i] += faceValue
    return C
#######################################2#######################################














