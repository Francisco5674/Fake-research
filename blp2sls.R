########### 2sls demand estimation ##################
library(data.table)
library(lfe)
source("dummy_columns.R")

data <- fread("nevo.csv")

# getting s0
share0 <- data[,.(s0 = 1 - sum(shares)), by = "market_ids"]
data <- merge(data, share0, by = "market_ids")

# gettin y = log(sj) - log(s0)
data$ds <- log(data$shares) - log(data$s0)

# covariance restrictions
# getting P*
starpstage <- lm(prices ~ factor(market_ids) + factor(product_ids), data = data)
Pstar <- starpstage$residuals
alphaOLS <- cov(Pstar,data$ds)/var(Pstar)
OLSres <- data$ds - alphaOLS*Pstar
lambda <- 1/(1 - data$shares)

## first componnent
comp_I <- cov(Pstar,lambda)/var(Pstar) - alphaOLS

## second componnent
comp_II <- - alphaOLS * cov(Pstar,lambda)/var(Pstar) - cov(OLSres,lambda)/var(Pstar)

coeff <- (-comp_I - sqrt(comp_I^2 - 4*comp_II))/2

# Elasticity
print("Elasticity")
print(coeff*mean(data$prices*(1 -data$shares)))
