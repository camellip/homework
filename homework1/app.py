from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/orderform', methods=['POST'])
def write_order():
    name_receive = request.form['name_give']
    qty_receive = request.form['qty_give']
    address_receive = request.form['address_give']
    tel_receive = request.form['tel_give']

    # DB에 삽입할 order 만들기
    doc = {
       'name': name_receive,
       'qty': qty_receive,
       'address': address_receive,
       'tel': tel_receive
    }
    # orderform에 order 저장하기
    db.orderform.insert_one(doc)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '주문이 성공적으로 접수되었습니다.'})


@app.route('/orderform', methods=['GET'])
def read_order():
		# 1. DB에서 리뷰 정보 모두 가져오기
    orders = list(db.orderform.find({},{'_id':0}))
		# 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'orderList': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)