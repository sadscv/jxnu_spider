from flask import Flask
from flask import request
from py_student import *
app = Flask(__name__)

@app.route('/')
def index():
  with open("find.html","r",encoding="UTF-8") as f:
    return f.read()
@app.route('/search')
def search():
  login("201626203044","362421199712231412")
  # callback=request.args.get("callback")
  name=request.args.get("name")
  return search_people(name)
  # data=search_people(name)
  # return callback+'('+data+')';

@app.route('/kebiao')
def get_kebiao():
  # callback=request.args.get("callback")
  xuehao=request.args.get("xuehao")
  return get_other_kebiao(xuehao)
  # data=get_other_kebiao(xuehao)
  # return callback+'('+data+')';

if __name__ == '__main__':
    app.run(host='0.0.0.0',port="8888")