from waitress import serve
import flask_template

if __name__ == '__main__':
    serve(flask_template.app, host='0.0.0.0', port=5000)