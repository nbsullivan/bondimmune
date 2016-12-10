# KEY RATE DURATION FUNCTIONS
#    Calculate key rate durations of individual bonds and/or portfolios
#     assuming yields are zero-coupon rates compounded continuously.
#    Modified to work within a pandas dataframe and dictionaries.
#
# 15 November 2016
# Anthony Gusman
#
# References:
#    Nawalkha, Soto, and Beliaeva. 2005. Interest Rate Risk Modeling: The 
#       Fixed Income Valuation Course. John Wiley & Sons, Inc. New Jersey.



import numpy as np                               # MATLAB-style functions
from datetime import date
from dateutil.relativedelta import relativedelta


def krdprepare(bond,currentTime,keyrates,mode='disc'):
    # Prepares bond-position object for use with krd functions.
    #  Will also be used to control keyrates for mismatched.
    if keyrates=='default':
        CF = np.copy(bond["couponpayments"]);    c0 = CF.size
        M = np.array([relativedelta(cdate,currentTime).months 
                      for cdate in bond["coupondates"]])
        YM = 12*np.array([relativedelta(cdate,currentTime).years 
                      for cdate in bond["coupondates"]])
        T = YM + M
        Y = effI(bond["interestrate"],mode=mode)
        if type(Y)==float or Y.size==1:
            Y = Y * np.ones(c0)            
        CF[T<=0] = 0;
        return T, CF, Y
   
    
    
def effI(annY,n=12,mode='disc'):
    # Input interest per annum, output nominal per annum
    if mode=='disc':
        effmY = ((1+annY)**(1./n) - 1)
    elif mode=='cont':
        effmY = annY
    return effmY
#######################################0#######################################

 # GATEWAY FUNCTION   
def krdbond(bond,currentTime=None,keyrates='default',mode='disc',indiv=False):
#   Computes key rate durations of cash flows.
#    T    Term structure;  vector 1-by-N
#    CF   Cash flow;       vector 1-by-N
#    Y    Yield structure; vector 1-by-N
    if currentTime == None:
        currentTime = bond["createdate"]
    T, CF, Y = krdprepare(bond,currentTime,keyrates,mode)    
    P = pvalcf(T,CF,Y,mode,indiv=indiv)
    Psum = np.sum(P)
    if mode=='cont':
        if Psum==0:
            KRD = np.zeros(CF.size)
        else:
            KRD = 1/P * CF*T/np.exp(Y*T)
    elif mode=='disc':
        if Psum==0:
            KRD = np.zeros(CF.size)
        else:
            KRD = 1/P * CF*T/((1+Y)**(T+1))
    KRD = KRD/12                                             # report in years
    return KRD,P

    
     
def pvalcf(T,CF,Y,mode='disc',indiv=False):
#   Computes present value of cash flows.
#    T    Term structure;  vector 1-by-N  (months)
#    CF   Cash flow;       vector 1-by-N
#    Y    Yield structure; vector 1-by-N  (monthly effective rate)
    if mode=='cont':
        s = CF/np.exp(Y*T)
    elif mode=='disc':
        s = CF/((1+Y)**T)
    if indiv==False:
        P = np.sum(s)
    elif indiv==True:
        P = s
    return P
#######################################1#######################################


def krdport(portfolio,currentTime=None,keyrates='default',mode='disc'):
#   Computes key rate duration of portfolio. Requires input bonds to have same 
#    payment length (i.e., padding with zeros). This requirement will be
#    handled by krdprepare.py
    BONDS = portfolio.to_dict('records')
    b = len(BONDS)
    KRD = []                            
    W = []
    P = []
    for bond in BONDS:
        KRD = np.append(KRD,krdbond(bond,currentTime,mode=mode)[0]);  
        W = np.append(W,bond["weight"])
        P = np.append(P,krdbond(bond,currentTime,mode=mode)[1])
    KRD = KRD.reshape(b,len(KRD)/b)
    S = W*np.transpose(KRD)
    KRDport = np.sum(S,1)
    return KRDport,P
    
    

#######################################2#######################################











