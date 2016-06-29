setwd("C:\\Users\\sime\\PycharmProjects\\diplomska-lol")
library(ipred)
library(neuralnet)
data = read.table("data_composition_diamond_challenger.tab", sep="\t", header=TRUE,stringsAsFactors=FALSE)
data[1:2] <-list(NULL)
data[data$winner=="blue","winner"]<- 0
data[data$winner=="red","winner"]<- 1
data$winner <- as.numeric(as.character(data$winner))

CA <- function(observed, predicted)
{
	t <- table(observed, predicted)

	sum(diag(t)) / sum(t)
}
testI = sample(1:nrow(data), size = 10000, replace=F)
test = data[testI,]
learn = data[-testI,]
sizes = c(1)
decay = c(0.1)
test_CA = array(0,c(length(sizes),length(decay)))
learn_CA = array(0,c(length(sizes),length(decay)))
#winner ~ .         not accepted?
n <- names(data)
f <- as.formula(paste("winner ~", paste(n[!n %in% "winner"], collapse = " + ")))
for(i in 1:length(sizes)){
	for(j in 1:length(decay)){
	  learn2 = learn[sample(1:nrow(learn), size = 90000, replace=F),]
	  nn <- neuralnet(f, data=learn2, hidden =c(5,4,2),linear.output=FALSE,lifesign="full",threshold=0.05,stepmax=20000)


	  predicted_l <- compute(nn, learn2[,1:ncol(learn2)-1])$net.result
	  predicted_t <- compute(nn, test[,1:ncol(test)-1])$net.result
	  learn_CA[i,j] = CA(learn2$winner, round(predicted_l))
	  test_CA[i,j] = CA(test$winner, round(predicted_t))
	}
}


plot(sizes, learn_CA,type="l",ylim=c(0.5,1), col="blue",ylab="CA")
par(new=TRUE)
lines(sizes, test_CA, axes=FALSE, xlab = "",ylab="", col="red")
