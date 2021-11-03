### 데이터의 대략적인 특징 파악

head(Orange)
head(Orange, 3)

tail(Orange)
tail(Orange, 10)

str(Orange)
summary(Orange)

### 외부파일 읽기

## CSV 파일 불러오기
nhis = read.csv("c:/data/NHIS_OPEN_GJ_EUC-KR.csv", fileEncoding = "EUC-KR")
nhis = read.csv("c:/data/NHIS_OPEN_GJ_UTF-8.csv", fileEncoding = "UTF-8")
sample = read.csv("c:/data/sample.csv", header = F,
                  fileEncoding = "EUC-KR",stringsAsFactors = TRUE)

##엑셀 파일 불러오기

install.packages("openxlsx")
library(openxlsx)

nhis_sheet1 = read.xlsx("c:/data/NHIS_OPEN_GJ_EUC-KR.xlsx")
nhis_sheet2 = read.xlsx("c:/data/NHIS_OPEN_GJ_EUC-KR.xlsx", sheet = 2)


#빅데이터 파일 불러오기
install.packages("data.table")
library(data.table)

nhis_bigdata = fread("c:/data/NHIS_OPEN_GJ_BIGDATA_UTF-8.csv", encoding = "UTF-8")
str(nhis_bigdata)

###데이터 추출

#행 인덱스를 이용하여 행 제한

Orange[1,]
Orange[1:5,]
Orange[6:10,]
Orange[c(1,5),]
Orange[-c(1:29),]

#데이터를 비교하여 행 제한
Orange[Orange$age == 118,]


#age 컬럼의 데이터가 118또는 484인 행만 추출
Orange[Orange$age %in% c(118,484),]

#age 컬럼의 데이터가 1372와 같거나 큰 행만 추출
Orange[Orange$age >= 1372,]

#열이름을 이용하여 열제한
Orange[, "circumference"]

# Orange의 Tree 와 circumference 열만 추출, 행은 1행만 추출
Orange[1 ,c("Tree","circumference")]

Orange[,1]
Orange[,c(1,3)]
Orange[,c(1:3)]
Orange[,-c(1,3)]

#행과 열제한

Orange[1:5 ,"circumference"]

#Tree 열이 3또는 2인 행의 Tree열과 circumference열 추출
Orange[Orange$Tree %in% c(3,2), c("Tree","circumference")]

#정렬
OrangeT1 = Orange[Orange$circumference < 50,]
OrnageT1[order(OrangeT1$circumference),]

#내림차순 정렬
OrnageT1[order(-OrangeT1$circumference),]

#그룹별 정렬
#Tree 별 circumference 평균
aggregate(circumference~Tree, Orange, mean)

#데이터 구조 변경

##데이터 준비
stu1 = data.frame(no = c(1,2,3), midterm = c(100,90,80))
stu2 = data.frame(no = c(1,2,3), finalterm = c(100,90,80))
stu3 = data.frame(no = c(1,4,5), quiz = c(99,88,77))
stu4 = data.frame(no = c(4,5,6), midterm = c(99,88,77))

#데이터 병합

merge(stu1, stu2)
merge(stu1, stu3)
merge(stu1, stu3, all =TRUE)
rbind(stu1, stu4)
cbind(stu1, stu2)









