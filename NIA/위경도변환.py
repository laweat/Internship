import pandas as pd
# csv파일 불러오기
csv = pd.read_csv('incheon_coffeeshop_20210805.csv',encoding='cp949')
print(csv.head())

# 데이터프레임 주소값 추출
address= csv['소재지도로명주소']
print(address.head())


# 주소 데이터 깔끔하게 다듬기
for i in range(len(address)):
    a = address[i].split(' ')
    address[i] = " ".join(a[0:4])
print(address)

####### 도로명주소 위도 경도 값으로 바꿔주기 ########
from geopy.geocoders import Nominatim
geo_local = Nominatim(user_agent='South Korea')
# 위도, 경도 반환하는 함수
def geocoding(address):
    geo = geo_local.geocode(address)
    x_y = [geo.latitude, geo.longitude]
    return x_y




#####주소를 위,경도 값으로 변환하기 #####
latitude = []
longitude =[]

for i in address:
    latitude.append(geocoding(i)[0])
    longitude.append(geocoding(i)[1])

#####Dataframe만들기######
address_df = pd.DataFrame({'카페이름': csv['사업장명'],'상세주소':csv['소재지도로명주소'],'주소':address,'위도':latitude,'경도':longitude})

#df저장
address_df.to_csv('jungu_incheon_coffeeshop.csv')
