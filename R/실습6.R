#주성분분석

#princomp()

#상관행렬 이용한 주성분 분석
fit = princomp(iris[,1:4], cor = TRUE)
summary(fit)

#loading()함수로 각 주성분의 로딩 벡터를 구하는 예
loadings(fit)

screeplot(fit, type = "lines", main = "scree plot")
