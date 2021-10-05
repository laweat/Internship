from flask import Flask, render_template, request, send_file, make_response, Response
app = Flask(__name__)


@app.route("/")
def hello():
    list_daum = [1,2,3,1,2,3,2,3,4,55,1,2,3,4]
    cnt = len(list_daum)
    return render_template("text.html", list_daum = list_daum , cnt= cnt)

if __name__ == '__main__':
    app.run()



