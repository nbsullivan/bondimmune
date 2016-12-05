library(ggplot2)
library(reshape)
# change working directory to your data file path.
setwd('/Users/nick/Documents/math503/project2/bondimmune')

# loading datasets
trimmed_df <- read.csv('trimmed_data.csv')
cleaned_df <- read.csv('cleaned_data.csv')

# date as a date object
trimmed_df$date <- as.Date(trimmed_df$date)
cleaned_df$date <- as.Date(cleaned_df$date)

#  better column names
newCnames <- c('X1.month' = 'month1', 'X3.month' = 'month3', 'X6.month' = 'month6', 'X1.year' = 'year1',
               'X2.year' = 'year2', 'X3.year' = 'year3', 'X5.year' = 'year5', 'X7.year' = 'year7',
               'X10.year' = 'year10','X20.year' = 'year20','X30.year' = 'year30')

trimmed_df <- rename(trimmed_df, newCnames)
cleaned_df <- rename(cleaned_df, newCnames)

# melted data for facet plotting
clean_rshp <- melt(cleaned_df, id = c ('daynumber', 'date'))

theme_set(theme_gray(base_size = 18))

reduced_df <- subset(trimmed_df, date > as.Date("2006-03-01") & date < as.Date("2016-02-29"))
ggplot(data = reduced_df, aes(x = date, y = year1)) +
  geom_line() +
  xlab('Date') +
  ylab('Interest Rate') +
  ggtitle('Interest Rates of 1 year bonds')

ggsave('1yearbondrates.pdf')



## anthonys yeild curve request.

rates <- c(	0.19,	0.28,	0.38,	0.5,	0.67,	0.76,	1.03,	1.29,	1.46,	1.78,	2.18)
maturities <- c( 1, 3, 6, 12, 24, 36, 60, 84, 120, 240, 360)
bondtype <- c(1:11)
ag_df <- data.frame(rates, maturities, bondtype)

ggplot(data = ag_df, aes(x = maturities, y = rates)) +
  geom_line() +
  geom_point() +
  ylab('Interest Rate (%)') +
  xlab('Maturity (Months)') +
  ggtitle('Yield curve for 7/29/2016')

ggsave('ag_yield_curve.pdf')


ggplot(data = ag_df, aes(x = bondtype, y = rates)) +
  geom_line() +
  geom_point() +
  scale_x_discrete(name ="Maturity (Months)", 
                   limits=c('1', '3', '6', '12','24','36','60','84','120','240','360' )) +
  ylab('Interest Rate (%)') +
  ggtitle('Yield curve for 7/29/2016')

ggsave('ag_yield_curve_alt.pdf')
