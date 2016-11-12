import krdur as krd
import numpy as np



# [1] Single bond present value and key rate durations
T = np.array([1,2,3,4,5])
Y = 1./100 * np.array([5,5.5,5.75,5.9,6])
CF = np.array([100,100,1100,0,0])

p = krd.pvalcf(T,CF,Y)
keybond = krd.krdbond(T,CF,Y)




# [2] Portfolio construction and key rate duration
#      Based on Example 9.1 of Nawalkha et al. (2005)
Bond1 = krd.cBond(1000,1,1,.10,fillTill=5)
Bond2 = krd.cBond(1000,2,1,.10,fillTill=5)
Bond3 = krd.cBond(1000,3,1,.10,fillTill=5)
Bond4 = krd.cBond(1000,4,1,.10,fillTill=5)
Bond5 = krd.cBond(1000,5,1,.10,fillTill=5)
    
class BONDS:
    T = np.array([1,2,3,4,5])
    Y = 1./100 * np.array([5,5.5,5.75,5.9,6])
    CF = np.array([Bond1,Bond2,Bond3,Bond4,Bond5])       

W = np.array([0.2,0.2,0.2,0.2,0.2])

keyport = krd.krdport(W,BONDS)