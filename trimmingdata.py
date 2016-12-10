import pandas as pd 


"""
Reduces the dataset from the cleaned FRB data to only include rows that are fully populated.
"""

if __name__ == '__main__':
	
	# load the cleaned dataset, it includes NaNs
	cleaned_df = pd.read_csv("cleaned_data.csv")

	# removed the rows that include and NaNs
	trimmed_df = cleaned_df.dropna()

	# write to file
	trimmed_df.to_csv("trimmed_data.csv")
