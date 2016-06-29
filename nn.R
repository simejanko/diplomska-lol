setwd("C:\\Users\\sime\\PycharmProjects\\diplomska-lol")
library(ipred)
library(neuralnet)
compositions = read.table("data_composition_diamond_challenger.tab", sep="\t", header=TRUE)

CA <- function(observed, predicted)
{
	t <- table(observed, predicted)

	sum(diag(t)) / sum(t)
}
testI = sample(1:nrow(compositions), size = 10000, replace=F)
test = compositions[testI,]
learn = compositions[-testI,]
test_CA = c()
learn_CA = c()
sizes = c(500, 2000, 5000, 10000,15000,25000,35000)
for(s in sizes)
{
  learn2 = learn[sample(1:nrow(learn), size = s, replace=F),]
  nn <- nnet(winner ~ ., data = learn2, size = 6, decay = 0, maxit = 1000, MaxNWts=6000)
  predicted_l <- predict(nn, learn2, type = "class")
  predicted_t <- predict(nn, test, type = "class")
  learn_CA = c(learn_CA, CA(learn2$winner, predicted_l))
  test_CA = c(test_CA, CA(test$winner, predicted_t))
}


plot(sizes, learn_CA,type="l",ylim=c(0.5,1), col="blue",ylab="CA")
par(new=TRUE)
lines(sizes, test_CA, axes=FALSE, xlab = "",ylab="", col="red")