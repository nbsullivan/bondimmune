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

theme_set(theme_bw(base_size = 22))

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
  
  print(fil)
  if(grepl('Alpha',fil)){
    
    # read alpha file transpose and remove header row.
    df <- read.csv(fil, header=FALSE)
    df <- t(df)
    df <- df[-c(1),]

    
    # setting up new columns as numerics and alpha
    alpha <- substr(fil, 1,nchar(fil)-4)
    alphanum <- substr(fil, nchar(fil)-6, nchar(fil)-4)
    print(alphanum)
    print(alpha)
    col1 <- as.numeric(df[,1])
    col2 <- as.numeric(df[,2])
    col3 <- as.numeric(df[,3])
    col4 <- as.numeric(df[,4])
    col5 <- as.numeric(df[,5])

    # load data into full_df
    new_df <- data.frame(idx = col1, databased = col2, vasicekbased = col3, krddata = col4, krdvasicek = col5, alpha = alpha)
    new_df$alpha <- alpha
    new_df$alphanum <- as.numeric(alphanum)
    full_df <- rbind(full_df,new_df)
    
    if(nchar(fil) < 14){
      print("ploting and saving")
      # plot transaction costs.
      ggplot(data = new_df, aes(x = idx)) +
       geom_line(aes(y = vasicekbased, linetype = "Duration Matching")) +
       geom_line(aes(y = krdvasicek, linetype = "Key Rate Duration")) +
       guides(linetype=guide_legend(title=NULL)) +
       xlab('Months') +
       ylab('Transaction Costs') +
       ggtitle(paste('Vasicek transaction costs, R = ', alphanum))
      
     ggsave(paste('visBW/BWvasicek',alpha,'.pdf', sep = ''))
    
     ggplot(data = new_df, aes(x = idx)) +
       geom_line(aes(y = databased, linetype = "Duration Matching")) +
       geom_line(aes(y = krddata, linetype = "Key Rate Duration")) +
       guides(linetype=guide_legend(title=NULL)) +
       xlab('Months') +
       ylab('Transaction Costs') +
       ggtitle(paste('Data transaction costs, R = ', alphanum))
     
     ggsave(paste('visBW/BWdata',alpha,'.pdf', sep = ''))
     
     # cumlative sums.
     new_df$cumdatabased <- cumsum(new_df$databased)
     new_df$cumkrddata <- cumsum(new_df$krddata)
     new_df$cumvasicekbased <- cumsum(new_df$vasicekbased)
     new_df$cumkrdvasicek <- cumsum(new_df$krdvasicek)
     
     ggplot(data = new_df, aes(x = idx)) +
       geom_line(aes(y = cumdatabased, linetype = "Duration Matching")) +
       geom_line(aes(y = cumkrddata, linetype = "Key Rate Duration")) +
       guides(linetype=guide_legend(title=NULL)) +
       xlab('Months') +
       ylab('Cumlative Transaction Costs') +
       ggtitle(paste('Cumulative Data costs, R = ', alphanum))
     
     ggsave(paste('visBW/cumBWdata',alpha,'.pdf', sep = ''))
     
     ggplot(data = new_df, aes(x = idx)) +
       geom_line(aes(y = cumvasicekbased, linetype = "Duration Matching")) +
       geom_line(aes(y = cumkrdvasicek, linetype = "Key Rate Duration")) +
       guides(linetype=guide_legend(title=NULL)) +
       xlab('Months') +
       ylab('Cumlative Transaction Costs') +
       ggtitle(paste('Cumulative Vasicek costs, R = ', alphanum))
     
     ggsave(paste('visBW/cumBWvasicek',alpha,'.pdf', sep = ''))
     
    }
    
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

rates_df <-subset(rates_df, ratetype == 'Data' | ratetype == 'Vasicek')
ggplot(data = rates_df, aes(x = idx, y = rate, linetype = ratetype)) +
  geom_line() +
  ylab('Interest Rate') +
  xlab('Months') +
  ggtitle('Vasicek interest rate model on 5 year bonds') +
  guides(linetype=guide_legend(title=NULL))


ggsave('visBW/BWVasicekperformance.pdf')

# total transaction costs as function of alpha.
vasicekaggmatch <- aggregate(full_df$vasicekbased, by=list(Alpha=full_df$alpha), FUN=sum)
vasicekaggmatch$type <- paste('Vasicek', substr(vasicekaggmatch$Alpha, 1, nchar(vasicekaggmatch$Alpha)-4), sep = '')
vasicekaggmatch$alphanum <-  as.numeric(substr(vasicekaggmatch$Alpha, nchar(vasicekaggmatch$Alpha)-2, nchar(vasicekaggmatch$Alpha)))

dataaggmatch <- aggregate(full_df$databased, by=list(Alpha=full_df$alpha), FUN=sum)
dataaggmatch$type <- paste('Data', substr(dataaggmatch$Alpha, 1, nchar(dataaggmatch$Alpha)-4), sep = '')
dataaggmatch$alphanum <-  as.numeric(substr(dataaggmatch$Alpha, nchar(dataaggmatch$Alpha)-2, nchar(dataaggmatch$Alpha)))


vasicekaggkrd <- aggregate(full_df$krdvasicek, by=list(Alpha=full_df$alpha), FUN=sum)
vasicekaggkrd$type <- paste('Vasicek', substr(vasicekaggkrd$Alpha, 1, nchar(vasicekaggkrd$Alpha)-4), sep = '')
vasicekaggkrd$alphanum <-  as.numeric(substr(vasicekaggkrd$Alpha, nchar(vasicekaggkrd$Alpha)-2, nchar(vasicekaggkrd$Alpha)))

dataaggkrd <- aggregate(full_df$krddata, by=list(Alpha=full_df$alpha), FUN=sum)
dataaggkrd$type <- paste('Data', substr(dataaggkrd$Alpha, 1, nchar(dataaggkrd$Alpha)-4), sep = '')
dataaggkrd$alphanum <-  as.numeric(substr(dataaggkrd$Alpha, nchar(dataaggkrd$Alpha)-2, nchar(dataaggkrd$Alpha)))




agg_dfmatch <- rbind(vasicekaggmatch,dataaggmatch)

# breaking down into components
# gamma = R
aggmatchVR <- subset(agg_dfmatch, type == 'VasicekAlpha')
aggmatchDR <- subset(agg_dfmatch, type == 'DataAlpha')
aggmatchR <- rbind(aggmatchVR, aggmatchDR)

# gamma = R^2
aggmatchVR2 <- subset(agg_dfmatch, type == 'Vasicekpow2Gamma_Alpha')
aggmatchDR2 <- subset(agg_dfmatch, type == 'Datapow2Gamma_Alpha')
aggmatchR2 <- rbind(aggmatchVR2, aggmatchDR2)

# gamma = sqrt(R)
aggmatchVsqrtR <- subset(agg_dfmatch, type == 'VasiceksqrtGamma_Alpha')
aggmatchDsqrtR <- subset(agg_dfmatch, type == 'DatasqrtGamma_Alpha')
aggmatchRsqrtR <- rbind(aggmatchVsqrtR, aggmatchDsqrtR)


ggplot(data = aggmatchR, aes(x = alphanum, y = x, linetype = type)) +
  geom_line() +
  xlab('R level') +
  ylab('Total transaction costs') +
  ggtitle( expression(paste('Transaction costs Duration Matching ',gamma == R), sep ='')) +
  guides(linetype=guide_legend(title=NULL)) +
  scale_linetype_discrete(labels = c('Data', 'Vasicek'))


ggsave('visBW/BWTransactioncostsRMatching.pdf')    

ggplot(data = aggmatchR2, aes(x = alphanum, y = x, linetype = type)) +
  geom_line() +
  xlab('R level') +
  ylab('Total transaction costs') +
  ggtitle( expression(paste('Transaction costs Duration Matching ',gamma == R^2), sep ='')) +
  guides(linetype=guide_legend(title=NULL)) +
  scale_linetype_discrete(labels = c('Data', 'Vasicek'))

ggsave('visBW/BWTransactioncostsR2Matching.pdf')   
    

ggplot(data = aggmatchRsqrtR, aes(x = alphanum, y = x, linetype = type)) +
  geom_line() +
  xlab('R level') +
  ylab('Total transaction costs') +
  ggtitle( expression(paste('Transaction costs Duration Matching ',gamma == sqrt(R)), sep ='')) +
  guides(linetype=guide_legend(title=NULL)) +
  scale_linetype_discrete(labels = c('Data', 'Vasicek'))


ggsave('visBW/BWTransactioncostssqrtRMatching.pdf')   

    




agg_dfkrd <- rbind(vasicekaggkrd,dataaggkrd)

# breaking down into components
# gamma = R
aggkrdVR <- subset(agg_dfkrd, type == 'VasicekAlpha')
aggkrdDR <- subset(agg_dfkrd, type == 'DataAlpha')
aggkrdR <- rbind(aggkrdVR, aggkrdDR)

# gamma = R^2
aggkrdVR2 <- subset(agg_dfkrd, type == 'Vasicekpow2Gamma_Alpha')
aggkrdDR2 <- subset(agg_dfkrd, type == 'Datapow2Gamma_Alpha')
aggkrdR2 <- rbind(aggkrdVR2, aggkrdDR2)

# gamma = sqrt(R)
aggkrdVsqrtR <- subset(agg_dfkrd, type == 'VasiceksqrtGamma_Alpha')
aggkrdDsqrtR <- subset(agg_dfkrd, type == 'DatasqrtGamma_Alpha')
aggkrdRsqrtR <- rbind(aggkrdVsqrtR, aggkrdDsqrtR)


ggplot(data = aggkrdR, aes(x = alphanum, y = x, linetype = type)) +
  geom_line() +
  xlab('R level') +
  ylab('Total transaction costs') +
  ggtitle( expression(paste('Transaction costs KRD ',gamma == R), sep ='')) +
  guides(linetype=guide_legend(title=NULL)) +
  scale_linetype_discrete(labels = c('Data', 'Vasicek'))

ggsave('visBW/BWTransactioncostsRkrd.pdf')    

ggplot(data = aggkrdR2, aes(x = alphanum, y = x, linetype = type)) +
  geom_line() +
  xlab('R level') +
  ylab('Total transaction costs') +
  ggtitle( expression(paste('Transaction costs KRD ',gamma == R^2), sep ='')) +
  guides(linetype=guide_legend(title=NULL)) +
  scale_linetype_discrete(labels = c('Data', 'Vasicek'))

ggsave('visBW/BWTransactioncostsR2krd.pdf')   


ggplot(data = aggkrdRsqrtR, aes(x = alphanum, y = x, linetype = type)) +
  geom_line() +
  xlab('R level') +
  ylab('Total transaction costs') +
  ggtitle( expression(paste('Transaction costs KRD ',gamma == sqrt(R)), sep ='')) +
  guides(linetype=guide_legend(title=NULL)) +
  scale_linetype_discrete(labels = c('Data', 'Vasicek'))


ggsave('visBW/BWTransactioncostssqrtRkrd.pdf')   



ggplot(data = agg_dfkrd, aes(x = alphanum, y = x, linetype = type)) +
  geom_line() +
  xlab('R level') +
  ylab('Total transaction costs') +
  ggtitle('Transaction costs of KRD') +
  guides(linetype=guide_legend(title=NULL)) +
  scale_linetype_discrete(labels = c(expression(paste('Data, ', gamma == R, sep = '')), 
                                  expression(paste('Data, ', gamma == R^2, sep = '')),
                                  expression(paste('Data, ', gamma == sqrt(R), sep = '')),
                                  expression(paste('Vasicek, ', gamma == R, sep = '')),
                                  expression(paste('Vasicek, ', gamma == R^2, sep = '')),
                                  expression(paste('Vasicek, ', gamma == sqrt(R), sep = ''))))


ggsave('visBW/BWTransactioncostsAlphaKRD.pdf')


ggplot(data = agg_dfmatch, aes(x = alphanum, y = x, linetype = type)) +
  geom_line() +
  xlab('R level') +
  ylab('Total transaction costs') +
  ggtitle('Transaction costs of KRD') +
  guides(linetype=guide_legend(title=NULL)) +
  scale_linetype_discrete(labels = c(expression(paste('Data, ', gamma == R, sep = '')), 
                                     expression(paste('Data, ', gamma == R^2, sep = '')),
                                     expression(paste('Data, ', gamma == sqrt(R), sep = '')),
                                     expression(paste('Vasicek, ', gamma == R, sep = '')),
                                     expression(paste('Vasicek, ', gamma == R^2, sep = '')),
                                     expression(paste('Vasicek, ', gamma == sqrt(R), sep = ''))))


ggsave('visBW/BWTransactioncostsAlphaMAtch.pdf')

