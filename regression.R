library(readr)
library(MLmetrics)
library(rpart)
library(tidyverse)
library(rsample)
library(ipred)       # bagging
library(caret)       # bagging

df <- read_csv('dataset_encoded_all_size.csv')
df <- dplyr::filter(df, cid >= 30000)
df <- dplyr::filter(df, vmlinux != -1)
df$nbyes <- rowSums(df == 1)
df$nbno <- rowSums(df == 0)
df$nbmodules <- rowSums(df == 2)

set.seed(42)
dat_split <- initial_split(df, prop = .15)
df_train <- training(dat_split)
df_test  <- testing(dat_split)
# m1 <- rpart(vmlinux~.-`LZ4`-`LZ4-bzImage`-`LZ4-vmlinux`-`BZIP2`-`BZIP2-bzImage`-`BZIP2-vmlinux`-`GZIP`-`GZIP-bzImage`-`GZIP-vmlinux`-`XZ`-`XZ-bzImage`-`XZ-vmlinux`-`LZO`-`LZO-bzImage`-`LZO-vmlinux`-`LZMA`-`LZMA-bzImage`-`LZMA-vmlinux`, data=df_train, method  = "anova")

bagged_m1 <- bagging(formula=vmlinux~.-`LZ4`-`LZ4-bzImage`-`LZ4-vmlinux`-`BZIP2`-`BZIP2-bzImage`-`BZIP2-vmlinux`-`GZIP`-`GZIP-bzImage`-`GZIP-vmlinux`-`XZ`-`XZ-bzImage`-`XZ-vmlinux`-`LZO`-`LZO-bzImage`-`LZO-vmlinux`-`LZMA`-`LZMA-bzImage`-`LZMA-vmlinux`, data=df_train, coob=TRUE)
print(bagged_m1)
ma <- MAPE(predict(bagged_m1, df_test), df_test$vmlinux)
print(ma)


# Specify 10-fold cross validation
# ctrl <- trainControl(method = "cv",  number = 2) 

# CV bagged model
# bagged_cv <- train(formula=vmlinux~.-`LZ4`-`LZ4-bzImage`-`LZ4-vmlinux`-`BZIP2`-`BZIP2-bzImage`-`BZIP2-vmlinux`-`GZIP`-`GZIP-bzImage`-`GZIP-vmlinux`-`XZ`-`XZ-bzImage`-`XZ-vmlinux`-`LZO`-`LZO-bzImage`-`LZO-vmlinux`-`LZMA`-`LZMA-bzImage`-`LZMA-vmlinux`, data=df_train, method = "treebag", trControl = ctrl, importance = TRUE)

# print(bagged_cv)
# ma_bag <- MAPE(predict(bagged_cv, ames_test), df_test$vmlinux)
# print(ma_bag)
# plot(varImp(bagged_cv), 20)  