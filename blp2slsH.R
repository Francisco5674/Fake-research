########### 2sls demand estimation ##################
library(data.table)
source("dummy_columns.R")

data <- fread("nevo.csv")

# getting s0
share0 <- data[,.(s0 = 1 - sum(shares)), by = "market_ids"]
data <- merge(data, share0, by = "market_ids")

# gettin y = log(sj) - log(s0)
data$ds <- log(data$shares) - log(data$s0)

# running model
firststage <- lm(formula = prices ~ demand_instrument
                            + factor(product_ids), data = data)
data$p_prices <- predict(firststage)
secondstage <- lm(formula = ds ~ p_prices + factor(product_ids), data = data)
