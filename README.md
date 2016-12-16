# bondimmune

Nicholas Sullivan, Anthony Gusman and Nathan Johnson.

Requirements: Python 2.7, pandas, SciPy, NumPy.


_Note: In the code "risk tolerance" is refered to as "alpha." This differs from the paper's use of alpha to refer to the transactional cost._

### To Run:
Run the script **bond_project.py** that will generate the data CSVs

For charts, use the **startingvis.R** script

### Function Collections:
* **my_immunization.py** holds immunization functions relating to duration matching
* **krdur.py** holds functions relating to key rate durations
* **bond_project_funs.py** holds functions relating to the flow of the script in bond_projects.
* _portfoliofuns.py_ is an outdated collection of functions based on an older model of storing bond/portfolio information

### Other scripts:
* **loadingdata.py** and **trimmingdata.py** load and reformat the data set from the Fed.
* _dataVis.m_ a small matlab visualization function, not used.

### .csv files:
The csv files included contain data relating to transactional costs for different gamma functions, also Vasicek_Rates.csv and Data_Rates.csv keep track of the interest rates for either the true data or the vasicek model rates.




