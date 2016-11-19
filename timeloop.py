import pandas as pd
import portfoliofuns
import krdur_pd
from pprint import pprint as pp
import numpy as np 


"""
time loop to check performance of portfolios over time.
"""



if __name__ == '__main__':
	

	trimmed_df = pd.read_csv("trimmed_data.csv")

	# because there are some where data has been removed we 
	# want to make sure that we don't accidentily call to an index position where no data exists.
	index_list = list(trimmed_df.index)


	# TODO a build portfolio function Nathan can you do this?
	# portfolio = portfoliofuns.buildportfolio()


	"""
	I do not think that we will need to deal with the entire time frame at once, so for a given case study
	we will want to look at a smaller range of dates aside from the full dataset. Also if we want to look at some important
	areas (1970s rate hikes?) we shouldn't use the trimmed data set, but thankfully portfoliofuns.todays_rates() returns only the rates
	that are avaliable during a day even if some are missing (this is dependent on the dataset used, if nothing is passed to 
	todays_rates then it uses the full fed dataset). We should identify 3-4 time periods of interesting rate changes, or boring rate changes
	to test the immunization stragies.
	"""
	# the actaul loop where things are going down.
	for daynum in index_list:

		# grab the current rates
		rates = portfoliofuns.todays_rates(daynumber = daynum, interestrate_df = trimmed_df)

		"""
		This is where the immunization code will go.

		Things to keep in mind:
		- if we are using stocastic methods make sure we set the seed so we can repeat expierments.
		- we will want to store the results of whatever we are doing, preferably in a .csv file.
		- a goodway to do that is to create a list of dictionaries which can be then turned into a dataframe and saved after the loop
		- Nick has no idea how to write this part.
		"""

