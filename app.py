from flask import Flask, redirect, url_for, request, render_template, flash
import main
import json
app = Flask(__name__)
app.secret_key = '123456'


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@app.route('/login', methods=['POST'])
def login():
    xh = request.form['xh']
    mm = request.form['mm']
    dq = request.form['dq'] if request.form['cs'] else '浙江省 杭州市 钱塘区'
    tz = request.form['tz'] if request.form['cs'] else ''
    cs = request.form['cs'] if request.form['cs'] else '0'
    with open('./essentials.json', 'r', encoding='utf-8') as f:
        essentials = json.load(f)
    essentials['users'].append(
        {'username': xh, 'password': mm, 'location': dq, 'notify_id': tz, 'retries': cs})
    with open('./essentials.json', 'w', encoding='utf-8') as f:
        json.dump(essentials, f)
    return redirect(url_for('hello'))


@app.route('/go', methods=['POST'])
def go():
    flash(main.main(dev=True))
    return redirect(url_for('hello'))


if __name__ == '__main__':
    app.run(debug=True)
