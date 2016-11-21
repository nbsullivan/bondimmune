library(ggplot2)

# change working directory to your data file path.
setwd('/Users/nick/Documents/math503/project2/bondimmune')

# loading datasets
trimmed_df <- read.csv('trimmed_data.csv')
cleaned_df <- read.csv('cleaned_data.csv')

# we probably want to have date as a date object
trimmed_df$date <- as.Date(trimmed_df$date)
cleaned_df$date <- as.Date(cleaned_df$date)

ggplot(data = trimmed_df, aes(x = date)) +
  geom_line(aes(y = X1.month)) +
  geom_line(aes(y = X3.month)) +
  
  
  geom_line(aes(y = X3.month)) +
