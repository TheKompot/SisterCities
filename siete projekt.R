library(fitdistrplus)
library("VGAM")
stupen<- read.table("C:/Users/jaada/Desktop/siete .txt", quote="\"", comment.char="")
stupen<-sort(stupen[,1])
pagerank <- read.csv("C:/Users/jaada/Desktop/pagerank.txt", header=FALSE, quote="'")

pagerank[,2]<-as.numeric(pagerank[,2])
pagerank[which.max(pagerank[,2]),]

fit<-fitdist(stupen, "exp", "mle", discrete = TRUE)
gofstat(fit)
plot(fit)


fit<-fitdist(stupen, "pareto", start = list(shape = 3), discrete = TRUE, "mle", fix.arg = list(scale=1))
gofstat(fit)
plot(fit)


fit<-fitdist(stupen, "zeta",start = list(shape=0.5), discrete = TRUE, "mle")
gofstat(fit)
plot(fit)

