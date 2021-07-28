#####################################################################################################
# Script id   : 새올민원.R
# Script Name : 새올민원상담 분석 
# Input       : C:/01.Project/01.분석참조모델/Rscript/
#		00. Load R Sources.R / 01-1. Load Data.R / 01-2. Mapping.R / 02. Preprocessing(Online_Mobile).R / 03. EDA(Online_Mobile).R / 
#   04. SNA_dtm.R / 05-1-1. keyword_DT.R / 05-1-2. keyword_DTM.R / 05-2. keyword_arules.R
#   05-3-1. find_topic_N.R / 05-3-2. keyword_topic.R / 06-1. EDA_time.R / 06-2. assign_time.R
#   06-3. real_time.R / 06-4. delay_time.R / 09. tableau.R
#   load_library.R / preprocessing.R / morph_analysis.R / make_dtm.R
# Output      : C:/01.Project/01.분석참조모델/Result/
# Author      : 펜타시스템
#####################################################################################################
## 00. R 소스 불러오기 (Load R Sources)
#####################################################################################################
source('C:/01.Project/01.분석참조모델/Rscript/새올/00. Load R Sources.R', encoding = "UTF-8")

#####################################################################################################
## 01. 데이터 불러오기 및 정제 (Load Data Files)
#####################################################################################################
# 1) 데이터 정제 후 주소 및 처리부서 저장
source('C:/01.Project/01.분석참조모델/Rscript/새올/01-1. Load Data.R', encoding = "UTF-8")

# 2) 주소 및 처리부서 매핑 정보를 이용한 데이터 정제
source('C:/01.Project/01.분석참조모델/Rscript/새올/01-2. Mapping.R', encoding = "UTF-8")

#####################################################################################################
## 02. 데이터 전처리 (Data Preprocessing)
#####################################################################################################
source('C:/01.Project/01.분석참조모델/Rscript/새올/02. Preprocessing(Online_Mobile).R', encoding = "UTF-8")

#####################################################################################################
## 03. 현황분석 (EDA)
#####################################################################################################
source('C:/01.Project/01.분석참조모델/Rscript/새올/03. EDA(Online_Mobile).R', encoding = "UTF-8")

#####################################################################################################
## 04. 소셜 네트워크 분석 (SNA : Social Network Analysis)
#####################################################################################################
source('C:/01.Project/01.분석참조모델/Rscript/새올/04. SNA_dtm.R', encoding = "UTF-8")

#####################################################################################################
## 05. 특정 키워드 분석
#####################################################################################################
# 1) EDA
source('C:/01.Project/01.분석참조모델/Rscript/새올/05-1-1. keyword_DT.R', encoding = "UTF-8")
source('C:/01.Project/01.분석참조모델/Rscript/새올/05-1-2. keyword_DTM.R', encoding = "UTF-8")
re_DT_도로 <- keyword_DT(keyword = '도로')
dtm_도로 <- keyword_DTM(data = re_DT_도로, keyword = '도로')

# 2) 연관성 분석 (Association Rules Analytics)
source('C:/01.Project/01.분석참조모델/Rscript/새올/05-2. keyword_arules.R', encoding = "UTF-8")
keyword_aruls(dtm = dtm_도로, keyword = '도로', supp = 0.15, conf = 0.15)

# 3) 토픽 모델링 (Topic Modeling)
source('C:/01.Project/01.분석참조모델/Rscript/새올/05-3-1. find_topic_N.R', encoding = "UTF-8")
source('C:/01.Project/01.분석참조모델/Rscript/새올/05-3-2. keyword_topic.R', encoding = "UTF-8")
find_topic_N(dtm = dtm_도로)
k <- 5
keyword_topic(data = re_DT_도로, dtm = dtm_도로, k = k, keyword = '도로')

# 4) 현안 키워드 변경
# 주차
re_DT_주차 <- keyword_DT(keyword = '주차')
dtm_주차 <- keyword_DTM(data = re_DT_주차, keyword = '주차')
find_topic_N(dtm = dtm_주차)
k <- 2
keyword_topic(data = re_DT_주차, dtm = dtm_주차, k = k, keyword = '주차')

# 아파트
re_DT_아파트 <- keyword_DT(keyword = '아파트')
dtm_아파트 <- keyword_DTM(data = re_DT_아파트, keyword = '아파트')
find_topic_N(dtm = dtm_아파트)
k <- 2
keyword_topic(data = re_DT_아파트, dtm = dtm_아파트, k = k, keyword = '아파트')

#####################################################################################################
## 06. 민원처리 프로세스 분석
#####################################################################################################
# 1) 부서별 처리현황
source('C:/01.Project/01.분석참조모델/Rscript/새올/06-1. EDA_time.R', encoding = "UTF-8")
EDA_time(data = re_DT)

# 2) 담당자 지정시간 분석 
source('C:/01.Project/01.분석참조모델/Rscript/새올/06-2. assign_time.R', encoding = "UTF-8")
assign_time(data = re_DT, alpha = 2)

# 3) 순수 민원 처리 분석
source('C:/01.Project/01.분석참조모델/Rscript/새올/06-3. real_time.R', encoding = "UTF-8")
real_time(data = re_DT)

# 4) 연장 처리 분석
source('C:/01.Project/01.분석참조모델/Rscript/새올/06-4. delay_time.R', encoding = "UTF-8")
delay_time(data = re_DT)

#####################################################################################################
## 09. Tableau 데이터 저장
#####################################################################################################
source('C:/01.Project/01.분석참조모델/Rscript/새올/09. tableau.R', encoding = "UTF-8")
tableau(data = c('re_DT_도로', 're_DT_주차', 're_DT_아파트'))
#####################################################################################################
