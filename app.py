from flask import Flask, redirect, url_for, request, render_template, flash
import os
import datetime
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
    os.system('sed -i \'1s/=.*/={xh}/\' login.js'.format(xh=xh))
    os.system('sed -i \'2s/=.*/="{mm}"/\' login.js'.format(mm=mm))
    return redirect(url_for('hello'))


@app.route('/go', methods=['POST'])
def go():
    flash(os.popen('python3 robot.py').read())
    return redirect(url_for('hello'))


@app.route('/html', methods=['POST'])
def html():
    htmlpath = './log/' + str(datetime.date.today())+'.html'
    os.system('mv {path} ./log/right.html'.format(path=htmlpath))
    return redirect(url_for('hello'))


@app.route('/pic', methods=['POST'])
def pic():
    picpath = './log/' + str(datetime.date.today())+'.png'
    os.system('mv {path} ./log/right.png'.format(path=picpath))
    return redirect(url_for('hello'))


if __name__ == '__main__':
    app.run(debug=True)
