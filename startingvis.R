library(ggplot2)
library(reshape)
# change working directory to your data file path.
setwd('/Users/nick/Documents/math503/project2/bondimmune')

# loading datasets
trimmed_df <- read.csv('trimmed_data.csv')
cleaned_df <- read.csv('cleaned_data.csv')

# we probably want to have date as a date object
trimmed_df$date <- as.Date(trimmed_df$date)
cleaned_df$date <- as.Date(cleaned_df$date)

# also get better names
newCnames <- c('X1.month' = 'month1', 'X3.month' = 'month3', 'X6.month' = 'month6', 'X1.year' = 'year1',
               'X2.year' = 'year2', 'X3.year' = 'year3', 'X5.year' = 'year5', 'X7.year' = 'year7',
               'X10.year' = 'year10','X20.year' = 'year20','X30.year' = 'year30')
trimmed_df <- rename(trimmed_df, newCnames)
cleaned_df <- rename(cleaned_df, newCnames)

clean_rshp <- melt(cleaned_df, id = c ('daynumber', 'date'))


ggplot(data = trimmed_df, aes(x = date, y = year1)) +
  geom_line() +
  xlab('Date') +
  ylab('Interest Rate') +
  ggtitle('Interest Rates of 1 year bonds')

ggsave('1yearbondrates.pdf')
e