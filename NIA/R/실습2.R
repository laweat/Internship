###피어슨 상관계수 구하기
#Orange 데이터에서 나무의 둘레와 나무의 나이와의 피어슨 상관계수 구하기
cor(Orange$circumference, Orange$age)

#산점도 그래프
plot(Orange$circumference, Orange$age, col = "red", pch = 19)


#변수 간 상관계수 구하기
cor(iris[, 1:4])

#상관계수 검정
#피어슨 상관계수 검정
cor.test(iris$Petal.Length, iris$Petal.Width, method = "pearson")
#스피어만 상관계수 검정
#cor.test(첫 번째 변수, 두 번째 변수.Width, method = "spearman")

