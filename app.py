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
    essentials = {'username': xh, 'password': mm}
    with open('./essentials.json', 'w') as f:
        json.dump(essentials, f)
    return redirect(url_for('hello'))


@app.route('/go', methods=['POST'])
def go():
    flash(main.main())
    return redirect(url_for('hello'))


if __name__ == '__main__':
    app.run(debug=True)
