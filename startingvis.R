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

theme_set(theme_gray(base_size = 22))

reduced_df <- subset(trimmed_df, date > as.Date("2006-03-01") & date < as.Date("2016-02-29"))
ggplot(data = reduced_df, aes(x = date, y = year1)) +
  geom_line() +
  xlab('Date') +
  ylab('Interest Rate') +
  ggtitle('Interest Rates of 1 year bonds')

ggsave('vis/1yearbondrates.pdf')



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

ggsave('vis/ag_yield_curve.pdf')


ggplot(data = ag_df, aes(x = bondtype, y = rates)) +
  geom_line() +
  geom_point() +
  scale_x_discrete(name ="Maturity (Months)", 
                   limits=c('1', '3', '6', '12','24','36','60','84','120','240','360' )) +
  ylab('Interest Rate (%)') +
  ggtitle('Yield curve for 7/29/2016')

ggsave('vis/ag_yield_curve_alt.pdf')


## results stuffs.

files = list.files(pattern="*.csv")

full_df <- data.frame(idx = numeric(0), databased = numeric(0), vasicekbased = numeric(0), krddata = numeric(0), krdvasicek = numeric(0))
rates_df <- data.frame(idx = numeric(0), ratetype = character(0), rate = numeric(0))
for(fil in files){
  
  
  if(grepl('Alpha',fil)){
    
    # read alpha file transpose and remove header row.
    df <- read.csv(fil, header=FALSE)
    df <- t(df)
    df <- df[-c(1),]

    
    # setting up new columns as numerics and alpha
    alpha <- substr(fil, 7,nchar(fil)-4)
    col1 <- as.numeric(df[,1])
    col2 <- as.numeric(df[,2])
    col3 <- as.numeric(df[,3])
    col4 <- as.numeric(df[,4])
    col5 <- as.numeric(df[,5])

    # load data into full_df
    new_df <- data.frame(idx = col1, databased = col2, vasicekbased = col3, krddata = col4, krdvasicek = col5, alpha = alpha)
    new_df$alpha <- alpha
    full_df <- rbind(full_df,new_df)
    
    # plot transaction costs.
    ggplot(data = new_df, aes(x = idx)) +
      geom_line(aes(y = vasicekbased, color = "Duration Matching")) +
      geom_line(aes(y = krdvasicek, color = "Key Rate Duration")) +
      guides(color=guide_legend(title=NULL)) +
      xlab('Months') +
      ylab('Transaction Costs') +
      ggtitle(paste('Data based transaction costs, Alpha = ', alpha))
    ggsave(paste('vis/alphavasicek',alpha,'.pdf', sep = ''))
    
    ggplot(data = new_df, aes(x = idx)) +
      geom_line(aes(y = databased, color = "Duration Matching")) +
      geom_line(aes(y = krddata, color = "Key Rate Duration")) +
      guides(color=guide_legend(title=NULL)) +
      xlab('Months') +
      ylab('Transaction Costs') +
      ggtitle(paste('Vasicek based transaction costs, Alpha = ', alpha))
    ggsave(paste('vis/alphadata',alpha,'.pdf', sep = ''))
    
  }
  if(grepl('Rates',fil)){
    # working with Rates files.
    rdf <- read.csv(fil)
    
    # grab the 1 year interest rate and type.
    ratetype <- substr(fil,1,nchar(fil)-10)
    rates <- rdf[,8]
    idx <- c(1:84)
    rates_df <- rbind(rates_df, data.frame(idx = idx, ratetype = ratetype, rate = rates))
    
  }
  
}

# vasicek performance.
ggplot(data = rates_df, aes(x = idx, y = rate, color = ratetype)) +
  geom_line() +
  ylab('Interest Rate') +
  xlab('Months') +
  ggtitle('Vasicek interest rate model on 5 year bonds') +
  guides(color=guide_legend(title=NULL))

ggsave('vis/Vasicekperformance.pdf')

# total transaction costs as function of alpha.
vasicekaggmatch <- aggregate(full_df$vasicekbased, by=list(Alpha=full_df$alpha), FUN=sum)
vasicekaggmatch$type <- 'Vasicek'
dataaggmatch <- aggregate(full_df$databased, by=list(Alpha=full_df$alpha), FUN=sum)
dataaggmatch$type <- 'Data'
vasicekaggkrd <- aggregate(full_df$krdvasicek, by=list(Alpha=full_df$alpha), FUN=sum)
vasicekaggkrd$type <- 'Vasicek'
dataaggkrd <- aggregate(full_df$krddata, by=list(Alpha=full_df$alpha), FUN=sum)
dataaggkrd$type <- 'Data'

agg_dfmatch <- rbind(vasicekaggmatch,dataaggmatch)
agg_dfmatch$Alpha <- as.numeric(agg_dfmatch$Alpha)

ggplot(data = agg_dfmatch, aes(x = Alpha, y = x, color = type)) +
  geom_line() +
  xlab('Alpha level') +
  ylab('Total transaction costs') +
  ggtitle('Transaction costs of Duration Matching') +
  guides(color=guide_legend(title=NULL))

ggsave('vis/TransactioncostsAlphaMatching.pdf')

agg_dfkrd <- rbind(vasicekaggkrd,dataaggkrd)
agg_dfkrd$Alpha <- as.numeric(agg_dfkrd$Alpha)

ggplot(data = agg_dfkrd, aes(x = Alpha, y = x, color = type)) +
  geom_line() +
  xlab('Alpha level') +
  ylab('Total transaction costs') +
  ggtitle('Transaction costs of KRD') +
  guides(color=guide_legend(title=NULL))

ggsave('vis/TransactioncostsAlphaKRD.pdf')
