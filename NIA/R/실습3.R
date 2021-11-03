#단순선형회귀, 모델생성
data(Orange)
head(Orange)

#lm()함수로 단순 선형휘귀 모델 생성
model = lm(circumference ~ age, Orange)
model

#회귀계수만 확인
coef(model)

#잔차
r = residuals(model)
r[0:4]

#fitted() 함수로 model이 예측한 값 구하기
f = fitted(model)

#residuals()함수로 잔차 구하기
r = residuals(model)

#예측한 값에 잔차를 더하여 실제값과 동일한지 확인
#예측한 값고 잔차 더하기
f[0:4] + r[0:4]

#위와 같이 다음의 실제 데이터와 동일함을 확인할 수 있다.
#실제값
Orange[0:4, 'circumference']

#잔차 제곱합 구하기
deviance(model)

#predict.lm()함수로 나이가 100인 나무의 둘레를 예측하기
#예측
predict.lm(model, newdata = data.frame(age=100))

#설명력 확인
summary(model)
# summary(model) == cor(Orange$circumference, Orange$age) ^ 2
cor(Orange$circumference, Orange$age) ^ 2
