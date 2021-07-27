#차분
n = head(Nile)
n

#diff()함수
#1차 차분
n.diff1 = diff(n, differences = 1)
n.diff1

#2차 차분
n.diff2 = diff(n, differences = 2)
n.diff2

#자기회귀 누적 이동 평균 모델
install.packages("forecast")
library(forecast)

auto.arima(Nile)

Nile.arima = arima(Nile, order = c(1,1,1))
Nile.arima

forecast(Nile.arima, h = 5)

plot(forecast(Nile.arima, h = 5))

#ldeaths 데이터 분해하여 분석
plot(ldeaths)

ldeaths.decomp = decompose(ldeaths)
plot(ldeaths.decomp)

#추세요인만 따로 확인해보기
ldeaths.decomp.trend = ldeaths.decomp$trend
plot(ldeaths.decomp.trend)

#계절성만 따로 확인
ldeaths.decomp.seasonal = ldeaths.decomp$seasonal
plot(ldeaths.decomp.seasonal)
