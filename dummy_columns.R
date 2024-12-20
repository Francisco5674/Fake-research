####### function to create dummies ####

dummy_columns <- function(info){
    x <- data.table()
    variables <- unique(info)
    for (item in variables){
        x[,as.character(item)] <- info == item
    }
    return(x)
}

