from flask import Flask, render_template
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import threading
from flask import request
import os
import time
import socket
 
import usingapp as uapp
app = Flask(__name__)

host = socket.gethostname()
ip_addr = socket.gethostbyname(host)

######메인화면
@app.route('/')
#초기화면
def main():
 
    path_dir = 'static\html'
    path_dir1 = 'static\keyword' 
    path_dir2 = 'static\cnt'
    
    file_list = os.listdir(path_dir)
    file_list1 = os.listdir(path_dir1)
    file_list2 = os.listdir(path_dir2)
    file_list = file_list[::-1]
    file_list1 = file_list1[::-1]
    file_list2 = file_list2[::-1]


    return render_template('index.html',
                            file_list = file_list,
                            file_list1 = file_list1,
                            file_list2 = file_list2,
                            ip_addr = ip_addr)

                    
 



@app.route('/result', methods = ['POST'])
def result():
    print("result")
    if request.method == 'POST':
        #입력 값 받기
        keyword = request.form['input1']
        num = int(request.form['input2'])

        # app.result(keyword, num)

        timestr = datetime.now().strftime("%Y%m%d-%H%M%S.%f")
        t = threading.Thread(target=create_html, args=(timestr, keyword, num, ))
        t.start()
        
        tmp = render_template('tomethod.html', pass_str=timestr)
        return tmp


@app.route('/method', methods=['GET', 'POST'])
def method():

    if request.method == 'GET': 
        pstr = request.args["num"]
        if os.path.isfile("./static/html/{0}/log.txt".format(pstr)):
            print(datetime.now(), "로그파일이 있습니다.")
        data = "데이터 없음"
        with open("./static/html/{0}/log.txt".format(pstr), "r", encoding='utf-8') as f:
            endinfo = f.readlines()[-1]

        with open("./static/html/{0}/log.txt".format(pstr), "r", encoding='utf-8') as f:            
            data = f.read()
        
        if endinfo == "end":
            return render_template('move.html', pass_str="/static/html/{0}/result.html".format(pstr))
        else:
            return render_template('status.html',
                                    pass_str=data, 
                                    ip_addr = ip_addr)

    return "데이터 없음"

def create_html(pstr, keyword, num, ):

    # tmp = [1,6,7,12]
    # if num not in tmp:
    #     num = 3

    if num == 1 :
        num = '1개월'
    elif num == 6 :
        num = '6개월'
    elif num == 7 :
        num = '7일'
    elif num == 12:
        num = '1년'
    else:
        num = "3개월"


    timestr = datetime.now().strftime("%Y%m%d-%H%M%S.%f")
    folderPath = './static/html/{0}'.format(pstr)
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    folderPath1 = './static/keyword/{}{}'.format(timestr,keyword) #키워드 폴더
    if not os.path.exists(folderPath1):
        os.makedirs(folderPath1)

    folderPath2 = './static/cnt/{}{}'.format(timestr,num) #개월수 폴더
    if not os.path.exists(folderPath2):
        os.makedirs(folderPath2)
    
    
    if num == '1개월':
        num = 1
    elif num == '6개월':
        num = 6
    elif num == '7일':
        num = 7
    elif num == '1년':
        num = 12
    else:
        num = 3

    with open("./static/html/{0}/log.txt".format(pstr), "w", encoding='utf-8') as f:
        f.write("start")

    uapp.create_html(pstr, keyword, num)

    with open("./static/html/{0}/log.txt".format(pstr), "w", encoding='utf-8') as f:
        f.write("\nend")        
    

@app.errorhandler(404)
def page_not_fount(error):
    
    return render_template('resultError.html',
                            ip_addr = ip_addr,
                            ),404

# if __name__ == '__main__':
#     app.run(host='0.0.0.0')