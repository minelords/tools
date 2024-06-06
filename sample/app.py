from flask import *
import requests
import mylogin
app = Flask(__name__)
#app
@app.route('/')
def home():
    username=request.args.get('username','Guest')
    return render_template('index.html',username=username)

users = {
    'admin': '123456',
    'guest': '654321'
}

@app.route('/login',methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/api',methods=['GET', 'POST'])
def api():
    email=request.args.get('email')
    url="http://142.171.234.219:5000/api/v1?email={}".format(email)
    response = requests.get(url)
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析JSON数据
        data = response.json()
        return jsonify(data)
    else:
        # 请求失败，打印错误信息
        print(f'请求失败，状态码：{response.status_code}')


@app.errorhandler(404)
def handle_404_error(err):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(debug=True) 