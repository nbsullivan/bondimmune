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
import my_immunization as im
'''
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
    '''
#######################################0#######################################
def pvalcf(T,CF,Y,mode='disc',indiv=False):
#   Computes present value of cash flows.
#    T    Term structure;  vector 1-by-N  (months)
#    CF   Cash flow;       vector 1-by-N
#    Y    Yield structure; vector 1-by-N  (monthly effective rate)
    if mode=='cont':
        S = CF/np.exp(Y*T)
    elif mode=='disc':
        S = CF/((1+Y)**T)
    if indiv==False:
        PV = np.sum(S)
    elif indiv==True:
        PV = s
    return PV
    

def bond(CF,Y):
    # Inputs in months, returns in years
    s = np.size(CF)
    T = np.arange(s)+1
    PV = pvalcf(T,CF,Y)
    KRD = (1/PV)*dBdY(T,CF,Y)
    
    mTy = (1./12)
    KRD = mTy*KRD
    return KRD, PV
    
    
def dBdY(T,CF,Y):    
    return CF*T*(1+Y)**(-T-1)
    
    
def portfolio(P,Y,Q):
    # Q  quantity of each investment   
    s = np.size(P[0])
    T = np.arange(s)+1  
      
    pv   = []
    for CF in P:
        pv   = np.append(pv,pvalcf(T,CF,Y))
    PV = np.sum(pv)  
    
    KRD = (1/PV)*dPdY(T,P,Y,Q)
    mTy = (1./12)
    KRD = mTy*KRD
    return KRD, PV
    
    
def dPdY(T,P,Y,Q):
    s = np.size(P[0])
    DBDY = []
    for CF in P:
        DBDY = np.append(DBDY,dBdY(T,CF,Y))
    DBDY = DBDY.reshape(len(DBDY)/s,s)
    dPdy = Q*DBDY.T         # np.sum( ,1)
    return dPdy
    
    
    
def dkinterp(T,K):
    # T   input terms
    # K   key rates
    dyTdyk1 = 1*(T<=K[0]) + (K[1]-T)*(1./(K[1]-K[0]))*( (K[0]<T)*(T<K[1]) ) + 0*(K[1]<=T)
    
    dyTdykm = 0*(T<=K[-2]) + (T-K[-2])*(1./(K[-1]-K[-2]))*( (K[-2]<T)*(T<K[-1]) ) + 1*(K[-1]<=T)
    
    dyTdyK = []
    dyTdyK = np.append(dyTdyK,dyTdyk1)
    
    if K.size >= 3:
        # Interior points
        K_INT = K[1:-1]
        for s in np.arange(K_INT.size)+1:
            dyTdyks = 0*( (T<=K[s-1])+(K[s+1]<=T) ) + finterp(T,K,s)*( (K[s-1]<T)*(T<K[s+1]) )
            
            dyTdyK = np.append(dyTdyK,dyTdyks)
    dyTdyK = np.append(dyTdyK,dyTdykm)
    dyTdyK = np.reshape(dyTdyK,(len(dyTdyK)/T.size,T.size))
    
    return dyTdyK
    
    

def finterp(T,K,s):
    fT = (T-K[s-1])*(1./(K[s]-K[s-1]))*(T<K[s]) +1*(T==K[s]) +(K[s+1]-T)*(1./(K[s+1]-K[s]))*(K[s]<T)
    return fT
            
    

'''
 # GATEWAY FUNCTION   
def krdbond(bond,Y,keyrates='default',mode='disc',indiv=False):
#   Computes key rate durations of cash flows.
#    T    Term structure;  vector 1-by-N
#    CF   Cash flow;       vector 1-by-N
#    Y    Yield structure; vector 1-by-N
    CF = bond;   c = CF.size;
    T = np.arange(c)+1;
    P = pvalcf(T,CF,Y,mode,indiv=indiv)
    Psum = np.sum(P)
    if mode=='cont':
        if Psum==0:
            KRD = np.zeros(c)
        else:
            KRD = 1/P * CF*T/np.exp(Y*T)
    elif mode=='disc':
        if Psum==0:
            KRD = np.zeros(c)
        else:
            KRD = 1/P * CF*T/((1+Y)**(T+1))
    KRD = KRD/12                                             # report in years
    return KRD,P
'''
    
     

#######################################1#######################################

'''
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
'''    
    

#######################################2#######################################











