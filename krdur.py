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



def krdbond(T,CF,Y,mode='disc'):
#   Computes key rate durations of cash flows.
#    T    Term structure;  vector 1-by-N
#    CF   Cash flow;       vector 1-by-N
#    Y    Yield structure; vector 1-by-N    
    P = pvalcf(T,CF,Y,mode)
    if mode=='cont':
        KRD = 1/P * CF*T/np.exp(Y*T)
    elif mode=='disc':
        n = 365
        KRD = 1/P * CF*T/((1+Y/n)**(n*T+1))
    return KRD

    
     
def pvalcf(T,CF,Y,mode='disc'):
#   Computes present value of cash flows.
#    T    Term structure;  vector 1-by-N
#    CF   Cash flow;       vector 1-by-N
#    Y    Yield structure; vector 1-by-N
    if mode=='cont':
        s = CF/np.exp(Y*T)
        P = np.sum(s)
    elif mode=='disc':
        n = 365
        s = CF/((1+Y/n)**(n*T))
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
    
    
'''
# Now defunct procedure. Originally intended to produce an arbitrary timing
#  vector T. Abandoned due to difficulties aligning with monthly step sizes.
    
def cBond(faceValue,matMonths,annualCouponNum,couponRate):
#   Constructs coupon bond. Assuming equally spaced payments.
#    faceValue         Face value of bond;  scalar
#    matMonths         Months to maturity;   scalar
#    annualCouponNum   Number of coupons per year;   scalar
#    couponRate        Coupon value as a percent of face value;   scalar
    n = int(np.round(matMonths*(1./12)*annualCouponNum))   # number of payments
    s = matMonths*(1./n)                                            # step size
    cc = couponRate * faceValue
    C = np.zeros((1,n));  T = np.zeros((1,n))
    for i in range(n):
        C[0,i] = cc;  T[0,i] = s*(i+1)
        if i==n-1:
            C[0,i] += faceValue 
    return C, T
'''
#######################################2#######################################
class cBond:
    def new(self,faceValue,matMonths,annualCouponNum,couponRate):
    #   Constructs coupon bond at monthly scale. Assuming equally spaced 
    #    payments. Also assuming annualCouponNum is a factor of 12 and that 
    #    matMonths is a multiple of this factor.
    #
    #    faceValue         Face value of bond;  scalar
    #    matMonths         Months to maturity;   scalar
    #    annualCouponNum   Number of coupons per year;   scalar
    #    couponRate        Coupon value as a percent of face value;   scalar
        if 12 % annualCouponNum != 0:
            raise RuntimeError('annualCouponNum must be a factor of 12')    
        k = 12/annualCouponNum
        if matMonths % k != 0:
            raise RuntimeError('matMonths must align with annualCouponNum')        
        cc = couponRate * faceValue
        C = np.zeros((1,matMonths))
        for i in np.arange(k-1,matMonths,k):
            C[0,i] = cc
            if i==matMonths-1:
                C[0,i] += faceValue 
        return C
    

    def shift(self,bond,startMonth,endMonth):
    #   Shifts coupon bond for alignment with other bonds and timing.
    #
    #    bond          Bond object constructed by .new function
    #    startMonth    Month bond timing begins (prepending 0s)
    #    endMonth      Month bond tracking ends (postpending 0s)
        prepend = np.zeros((1,startMonth-1))
        sbond = np.append(prepend,bond)
        if endMonth > bond.size:
            postpend = np.zeros((1,endMonth-bond.size))
            sbond = np.append(sbond,postpend)
        return sbond
#######################################3#######################################











