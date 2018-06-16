from flask import Flask, render_template, redirect, request
from qrcode import empower
# import uuid
import redis

app = Flask(__name__)

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

@app.route('/')
def index():
    return render_template('bb.html')
    
    
@app.route('/qrcode', methods=['GET', 'POST'])
def qrcode():
    url, lgToken, umid_token = empower()
    ip = request.remote_addr
    task_id = request.args.get('task_id')
    r.set("task_id", task_id)
    print('IP:{}的umid_token是:{}'.format(ip, umid_token))
    r.lpush("tokens", (lgToken, umid_token))
    # uuid = uuid.uuid1()
    return redirect(url)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')