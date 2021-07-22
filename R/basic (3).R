# 벡터
studentsAge <- c(11,12,13,20,15,21)
sutdentsAge
class(studentsAge)
length(studentsAge)

# 벡터 인덱싱
studentsAge[1]
studentsAge[3]
studentsAge[-1]

# 벡터 슬라이싱
studentsAge[1:3]
studentsAge[4:6]

# 벡터에 데이터 추가, 갱신신
score <- c(1,2,3)
score[1] <- 10
score[4] <- 4
score

#벡터의 데이터 타입
code <- c(1,12,"30")
class(code)
code

# 순열 생성
data <- c(1:10)
data

data1 = seq(1, 10)
data1

data2 = seq(1,10, by = 2)
data2

data3 = rep(1, times = 5)
data3

data4 = rep(1:3, each = 3)
data4

data5 = rep(1:3, times = 3)
data5

#행렬
var1 = c(1,2,3,4,5,6)

x1 = matrix(var1, nrow = 2, ncol = 3)
x1

x2 = matrix(var1, ncol = 2)
x2

# 일부 데이터만 접근
x1[1, ]
x1[, 1]
x1[2, 2]

# 행렬에 데이터 추가
x1
x1 = rbind(x1, c(10,10,10)) #행추가
x1 = cbind(x1, c(20,20,20)) #열추가
x1

#데이터프레임
no = c(10,20,30,40,50,60,70)
age = c(18,15,13,12,10,9,7)
gender = c("M","M","M","M","M","F","M")

#데이터 프레임 생성 예예
student = data.frame(no, age, gender)
student

#열의 이름과 행의 이름 확인
colnames(student)
rownames(student)

colnames(student) = c("no","나이","성별")
rownames(student) = c("A","B","C","D","E","F","G")

student


#다시 원래 영문 열 이름으로 수정
colnames(student) = c("no","age","gender")
student

#일부데이터만 접근
#데이터 프레임의 변수이름 $열 이름으로 특정 열에 접근
student$no
student$age

#열이름으로 특정 열에 접근하는 예
#대괄호 안에 열이름으로 특정 열에 접근하기
#대괄호 안에 콤마(,) 를 쓴 후 열이름을 쓴다.
student[,"no"]
student[,"age"]

#열 인덱스로 특정 열에 접근하는 예
student[,1]
student[,2]

#행 이름으로 특정 행만 접근하는 예
student["A",]

#행 인덱스로 특정 행만 접근하는 예
student[2,]

#행 인덱스, 열 인덱스 또는 행 이름, 열이름으로 데이터 접근
student[3,1]
student["A","no"]

#배열
var1 = c(1,2,3,4,5,6,7,8,9,10,11,12)

arr1 = array(var1, dim=c(2,2,3))
arr1

#리스트
vData = c("02-111-2222","01022223333")
mData = matrix(c(21:26), nrow = 2)
aData = array(c(31:36),dim=c(2,2,2))
dData = data.frame(address = c("seoul","busan"),
                   name = c("Lee","Kim"),stringsAsFactors = F)

listData = list(name= "홍길동",
                tel = vData,
                score1 = mData,
                score2 = aData,
                friends = dData
)

#리스트 이름$키

listData$name

listData$tel

#리스트이름[숫자]
listData[1]

