# KEY RATE DURATION FUNCTIONS
#    Calculate key rate durations of individual bonds and/or portfolios.
#
# 8 December 2016
# Anthony Gusman
#
# References:
#    Nawalkha, Soto, and Beliaeva. 2005. Interest Rate Risk Modeling: The 
#       Fixed Income Valuation Course. John Wiley & Sons, Inc. New Jersey.



import numpy as np                               # MATLAB-style functions
import scipy as sp
from scipy import optimize




###############################PRESENT VALUE###################################
def pvalcf(T,CF,Y,mode='disc',each=False):
    """Computes PV, present value of cash flows.
    
       Inputs:
        T    Time-to-cashflow ;  vector 1-by-N  (months)
        CF   Cash flow        ;  vector 1-by-N
        Y    Yield structure  ;  vector 1-by-N  (monthly effective rates)
     
       Notes: Y must be defined for all possible values of T. PV is computed
             relative to equivalent cash flows in risk-free bonds.
    """
    if mode=='cont':
        S = CF/np.exp(Y*T)                            # continuous compounding
    elif mode=='disc':
        S = CF/((1+Y)**T)                     # periodic compounding (default)
        
    if each==False:
        PV = np.sum(S)                # report PV of bond as a whole (default)
    elif each==True:
        PV = s                                    # report PV of each cashflow
        
    return PV
    

    
    
    
    
       
############################SENSITIVITY MATRICES###############################    
def dBdY(T,CF,Y,mode='disc'):    
    """Sensitivity N-vector of bond to risk-free rates; derived from PV.
    
       Inputs:
        T    Time-to-cashflow ;  vector 1-by-N  (months)
        CF   Cash flow        ;  vector 1-by-N
        Y    Yield structure  ;  vector 1-by-N  (monthly effective rates)
    """
    if mode=='cont':
        DBDY = CF*T/np.exp(Y*T)                       # continuous compounding
    elif mode=='disc':
        DBDY = CF*T/((1+Y)**(T+1))            # periodic compounding (default)
    return DBDY
    
     
def dPdY(T,P,Y):
    """Sensitivity N-by-(# of bonds) matrix of portfolio to risk-free rates; 
         depends on DBDY.
    
       Inputs:
        T    Time-to-cashflow ;  vector 1-by-N  (months)
        CF   Cash flow        ;  vector 1-by-N
        Y    Yield structure  ;  vector 1-by-N  (monthly effective rates)
    """
    n = nbonds(P)                               # number of bonds in portfolio
    
    DPDY = []
    if n > 1:
        for B_CF in P:
            DPDY = np.append(DPDY,dBdY(T,B_CF,Y))
        DPDY = DPDY.reshape(n,len(DPDY)/n)
    else:
        DPDY = dBdY(T,P,Y)
    
    return DPDY.T

    

    
    
    
    
    
    
    
    
###############################INTERPOLATION###################################
def rateinterp(M,windowSize,maxMonths):
    """Returns interpolated interest rates for all possible months.
       
       Inputs:
                 M    Monthly interest rates           ;  matrix D-by-S
        windowSize    Amount of history in current run
         maxMonths    Number of possible months
    """
    S = M.ix[windowSize-1]                                  # current schedule
    U = [float(S.index[i]) for i in range(S.size)]             # extract terms
    V = [float(S.values[i]) for i in range(S.size)]            # extract rates
    X = np.arange(maxMonths)+1                            # interpolated terms
    Y = np.interp(X,U,V)                                  # interpolated rates
    return Y



def dkinterp(T,K):
    """Returns S-by-N key rate interpolation matrix.
       
       Inputs:
        T    Terms            ;  vector 1-by-N  (months)
        K    Key rates        ;  vector 1-by-S  (months)
       
       Note: The ith row, jth column gives the sensitivities of the jth term
             to the ith key rate. 
    """
    # Special Cases:
        # First key rate.
    lesseq1 = lambda T,K : 1*(T<=K[0])
    betwee1 = lambda T,K : (K[1]-T)*(1./(K[1]-K[0]))*( (K[0]<T)*(T<K[1]) )
    moreeq1 = lambda T,K : 0*(K[1]<=T)
    dyTdyk1 = lesseq1(T,K) + betwee1(T,K) + moreeq1(T,K)
    
       # Last key rate.
    lesseqm = lambda T,K : 0*(T<=K[-2])
    betweem = lambda T,K : (T-K[-2])*(1./(K[-1]-K[-2]))*( (K[-2]<T)*(T<K[-1]) )
    moreeqm = lambda T,K : 1*(K[-1]<=T)
    dyTdykm = lesseqm(T,K) + betweem(T,K) + moreeqm(T,K)
    
    # Main Case:
    dyTdyK = []
    dyTdyK = np.append(dyTdyK,dyTdyk1)   
    
    outside = lambda T,K,s : 0*( (T<=K[s-1])+(K[s+1]<=T) )
    between = lambda T,K,s : finterp(T,K,s)*( (K[s-1]<T)*(T<K[s+1]) )
    if K.size >= 3:        
        K_INT = K[1:-1]                                      # Interior points
        for s in np.arange(K_INT.size)+1:
            dyTdyks = outside(T,K,s) + between(T,K,s)            
            dyTdyK = np.append(dyTdyK,dyTdyks)
            
    dyTdyK = np.append(dyTdyK,dyTdykm)
    dyTdyK = np.reshape(dyTdyK,(len(dyTdyK)/T.size,T.size))
    
    return dyTdyK
    
    

def finterp(T,K,s):
    """Interpolation function for dkinterp."""
    less = lambda T,K,s : (T-K[s-1])*(1./(K[s]-K[s-1]))*(T<K[s])
    equl = lambda T,K,s : 1*(T==K[s])
    more = lambda T,K,s : (K[s+1]-T)*(1./(K[s+1]-K[s]))*(K[s]<T)    
    fT = less(T,K,s) + equl(T,K,s) + more(T,K,s)
    return fT


    

    
    
    
    
    
    
###############################BONDS & PORTFOLIOS##############################    
def bond(CF,Y,K):
    """Returns two outputs: KRD, S-vector of durations at key rates K;
                             PV, present value of bond.
                             
       Inputs:
        CF   Cash flow        ;  vector 1-by-N
        Y    Yield structure  ;  vector 1-by-N  (monthly effective rates)
        K    Key rates        ;  vector 1-by-S  (months)
                      
       Note: Inputs in months, outputs in years.
    """
    s = np.size(CF)
    T = np.arange(s)+1                                      # time-to-cashflow

    PV = pvalcf(T,CF,Y)        # computed based on hypothetical risk-free rate
    
    DBDY = dBdY(T,CF,Y)     # sensitivity of bond cashflows to risk-free rates
    DK = dkinterp(T,K)                         # key rate interpolation matrix
    dBdYk = np.dot(DK,DBDY)       # interpolated sensitivity of bond cashflows
    
    mTy = (1./12)                            # month-to-year conversion factor
    KRD = mTy*(1/PV)*dBdYk
    return KRD, PV     
    

   
def portfolio(P,Y,Q,K):
    """Returns two outputs: KRD, S-by-(# of bonds) matrix of durations at key 
                                 rates K;
                             PV, present value of bond.
                             
       Inputs:
        P    Portfolio        ;  matrix (# of bonds)-by-N
        Y    Yield structure  ;  vector 1-by-N  (monthly effective rates)
        Q    Quantity         ;  vector 1-by-(# of bonds)
        K    Key rates        ;  vector 1-by-S  (months)
                      
       Note: Each column of KRD corresponds to an individual bond; there is a
             row for each key rate.
    """  
    s = tlen(P)                                             # length of time
    T = np.arange(s)+1                                      # time-to-cashflow
      
    pv   = []
    for CF in P:
        pv   = np.append(pv,pvalcf(T,CF,Y))
    PV = np.sum(pv)  
    
    DPDY = dPdY(T,P,Y)
    DK = dkinterp(T,K)
    dPdYk = np.dot(DK,DPDY)
    
    mTy = (1./12)                            # month-to-year conversion factor
    KRD = mTy*(1/PV)*np.sum(Q*dPdYk, 1)
    return KRD, PV
    

       
def nbonds(P):
    """Extracts number of bonds in a portfolio; or 1 if a single bond."""
    if len(P.shape) == 1:
        N = 1
    elif len(P.shape) == 2:
        N = int(P.shape[0])
    return N
 
    
def tlen(P):
    """Extracts length of time from portfolio"""
    try:
        s = np.shape(P)[1]
    except IndexError:
        s = np.size(P)                                           # time length
    return s
    
    
    
    
    
    
    
    
################################IMMUNIZATION###################################    
def immunize(Pa,Y,Qa,Pl,K,w0='null',r=0.5):
    """Returns two outputs:  q, a vector of liability quantities that should
                                 be shorted;
                           err, deviation from exact match.
                           
       Inputs:
        Pa   Asset portfolio       ;  matrix (# of assets)-by-N
        Y    Yield structure       ;  vector 1-by-N  (monthly effective rates)
        Qa   Asset quantity        ;  vector 1-by-(# of assets)
        Pl   Liability portfolio   ;  matrix (# of liabilities)-by-N
        K    Key rates             ;  vector 1-by-S  (months)
        w0   Initial weight guess  ;  vector 1-by-(# of liabilities)
        r    Liability-to-Asset value ratio
                                                
        Note: q consists of negative values to indicate shorting.
    """
    N = nbonds(Pl)                    # number of bonds in liability portfolio
    if w0 == 'null':
        w0 = np.zeros(N)     
    
    KRDa,PVa = portfolio(Pa,Y,Qa,K)                 # obtain key rate and PV's
    
    # obtain present values of each liability (ignoring KRDs)
    s = tlen(Pl)                                             # length of time
    T = np.arange(s)+1                                      # time-to-cashflow
    L = np.array([bond(Pl[j],Y,K)[1] for j in range(len(w0))])
    DLDY = dPdY(T,Pl,Y)                         # liability sensitivity matrix
    DK = dkinterp(T,K)
    dPdYk = np.dot(DK,DLDY)                                
    KRDl = (1./L)*dPdYk                    # liability key rate duration matrix
    
    A = KRDl                                  # system setup and initilization
    b = (1/r)*KRDa       
    w, err = immunize_solve(A,b,w0)                        # solve for weights
    
    # obtain present values of each liability (ignoring KRDs)
    q = -(1./L)*w*(r*PVa)                      # convert weights to quantities
    return q, err, w
        
    
    
        
def immunize_solve(A,b,x0):
    """Solves KRD-matching system (weight formulation)"""
    
    # Consider adjusting order of norm...
    ord = 1;
    func = lambda x : np.linalg.norm(np.dot(A,x)-b, ord=ord)
       
    cons = {'type':'eq', 'fun': lambda x: x.sum()-1 }  # weights must sum to 1
    bons = [(0,1) for i in range(len(x0))]   # weights must be between 0 and 1
    
    # Consider adjusting method...
    method = 'SLSQP'
    res  = sp.optimize.minimize(func,x0,method=method,
                                constraints=cons,bounds=bons,
                                options={'disp': True})
    x = res.x  
    err = res.fun
    return x, err
    
    