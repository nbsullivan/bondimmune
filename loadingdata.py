import pandas as pd

if __name__ == '__main__':
	
	# we are assuming that the data is in the following path
	interest_df = pd.read_csv('../data/FRB_H15.csv')

	# first set of rows are some non data information
	interest_df = interest_df.iloc[5:]

	# the columns given are pretty clunky so reduce them to something shorter, like the term of the bond.
	columnlist = list(interest_df.columns.values)


	newcolumnnames = ['date']
	k = 0
	for item in columnlist:

		if k != 0:
			newcolumnnames.append(item[44:-45].strip())
		k += 1


	interest_df.columns = newcolumnnames
	interest_df.set_index('date', inplace = True)
	interest_df.to_csv("cleaned_data.csv")

	print interest_df.head()

