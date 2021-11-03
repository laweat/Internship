#다중선형회귀, 모델생성

height_father <-c(180,172,150,180,177,160,170,165,179,159)
height_mother<- c(160,164,166,188,160,160,171,158,169,159)
height_son <- c( 180,173,163,184,165,165,175,168,179,160)

height = data.frame(height_father, height_mother, height_son)
head(height)

model = lm(height_son ~ height_father+height_mother, data= height)
model

coef(model)

#잔차
r = residuals(model)
r[0:4]

#잔차 제곱합
deviance(model)

#예측 (점 추정)
predict.lm(model, newdata = data.frame(height_father=170, height_mother= 160))

#예측 (구간 추정)
predict.lm(model, newdata = data.frame(height_father=170, height_mother= 160), interval = 
             "confidence")

#결정계수, 수정된 결정계수 및 F통계량, 잔차, 사분위수, 회귀계수 확인
summary(model)

#mpg를 종속변수로 하고, 나머지 모든 변수를 설명변수로 사용하는 회귀 모델
model = lm(mpg~., data = mtcars)

newModel = step(model, direction = "both")

#모델 진단 그래프
model = lm(mpg~ wt + qsec + am, data  = mtcars)
plot(model)
