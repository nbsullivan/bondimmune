# bondimmune

Nicholas Sullivan, Anthony Gusman and Nathan Johnson.

Requirements: python 2.7, pandas, scipy, numpy.


Notes: In the code risk tolerance is refered to as alpha, this alpha is the risk tolerance not the transactional cost as mentioned in the paper.

To Run:
run the script bond_project.py that will generate the data csvs

for charts, use the startingvis.R script

function collections:
my_immunization.py holds immunization functions relating to duration matching
krdur.py holds functions relating to key rate durations
bond_project_funs.py holds functions relating to the flow of the script in bond_projects.
portfoliofuns.py is a outdated collection of functions based on an older model as to how to store bond/portfolio information

Other scripts:

loadingdata.py and trimmingdata.py load and reformat the data set from the Fed.
dataVis.m a small matlab visualization function, not used.

.csv files:
the csv files included contain data relating to transactional costs for different gamma functions, also Vasicek_Rates.csv and Data_Rates.csv keep track of the interest rates for either the true data or the vasicek model rates.




