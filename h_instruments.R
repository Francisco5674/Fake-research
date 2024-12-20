########### identifying instruments ############

allinstruments <- data.table()
banned_ids <- c()
for (i in 1:nrow(data)){
    product <- data[i]
    # we filter the instruments
    instruments <- data[data$product_ids == product$product_ids 
                        & data$quarter == product$quarter] 

    if (length(instruments) > 0){
        hinstrument <- mean(instruments$prices)
    }
    else{
        hinstrument <- 0
        banned_ids <- c(banned_ids, product$product_ids)
    }

    allinstruments <- rbind(allinstruments, hinstrument)
}

colnames(allinstruments) <- c("demand_instrument")

data <- cbind(data, allinstruments)
data$demand_instrument[data$product_ids %in% banned_ids] <- 0
data <- na.omit(data)
