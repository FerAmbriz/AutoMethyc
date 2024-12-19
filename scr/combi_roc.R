library(tidyverse)
library(combiroc)
library(pROC)

args <- commandArgs(trailingOnly = TRUE)
input = args[1]

#================== Data preparation ==============#
df_combinations <-  read_csv(paste(input, '/logistic_regression_combination_outliers.csv', sep =''))
df <-  read_csv(paste(input, '/filtered_target.csv', sep =''))
df <- df %>% mutate_all(~replace_na(., 0))

df <- df %>% mutate(Chr_Start = paste(Chr, Start, sep = ":"))

print(head(df_combinations))
combinations = df_combinations[1, 1]
combinations = unlist(strsplit(as.character(combinations), "_"))


print('Selection ...')
print(combinations)

data_long <- df %>% filter(Chr_Start %in% combinations)
print(head(data_long))

#=============== combiroc ===============#
data_long <- data_long[,c(1, 2, 4, 6)]
colnames(data_long) <- c('ID', 'Class', 'Markers', 'Values')

data_long <- data_long %>% mutate(Markers = paste0("cg", Markers))


data <- data_long %>%
  pivot_wider(names_from = Markers, values_from = Values)

#data$n_combinacion <- as.numeric(data$n_combinacion)

print('Preparation')
print(head(data))

se_sp_custom <- function (data, combinations_table) 
{
    mks <- combinations_table
    names <- c()
    nclass <- unique(data$Class)
    SE_SP <- array(0, dim = c(dim(mks)[1], 2 * 2))
    for (i in 1:length(nclass)) {
        SE_SP[, i] <- round(mks[, i + 1] * 100/dim(t(data[data$Class == nclass[i], ]))[2], digits = 0)
        names[i] <- paste0("SE_", nclass[i])
        SE_SP[, i + 2] <- 100 - SE_SP[, i]
        names[i + 2] <- paste0("SP_", nclass[i])
    }
    SE_SP <- data.frame(SE_SP)
    rownames(SE_SP) <- rownames(mks)
    colnames(SE_SP) <- names
    n_markers <- rep(NA, dim(mks)[1])
    for (i in 1:dim(mks)[1]) {
        n_markers[i] <- str_count(mks$Markers[i], pattern = "-") + 
            1
    }
    SE_SP$count <- data.frame(n_markers)[, 1]
    colnames(SE_SP)[5] <- "#Markers"
    return(SE_SP)
}

tab <- combi(data, signalthr = 0, combithr = 1, case_class='cases')
print('Description')
print(head(tab))

print('ROC curves')
combinations <- sub(".*:", "cg", combinations)
print(head(combinations))

data <- data %>% mutate_all(~replace_na(., 0))

print(head(data))

reports <-roc_reports(data, markers_table = tab, 
                      case_class = 'cases', single_markers = combinations, 
                      selected_combinations = c( nrow(tab)-length(combinations) ))

metrics_roc <- reports$Metrics


roc_combined <- data.frame()
for (model_name in names(reports$Models)) {
    model <- reports$Models[[model_name]]
    roc_obj <- roc(data$Class, fitted(model))

    # Extraer los datos de la curva ROC
    roc_data <- data.frame(
        "1-specificity" = 1 - roc_obj$specificities,
        "sensitivity" = roc_obj$sensitivities,
        "model" = model_name
    )
    
    # Concatenar los datos al DataFrame combinado
    roc_combined <- rbind(roc_combined, roc_data)
}

print(head(roc_combined))
print(head(metrics_roc))

write.csv(roc_combined, paste(input, "/roc_combined.csv", sep = ''), row.names = FALSE)
write.csv(metrics_roc, paste(input, "/roc_metrics.csv", sep = ''))
