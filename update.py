import requests
res = requests.get(
    'https://raw.githubusercontent.com/typenoob/zstu_report/master/main.py')
with open('main.py', 'wb') as f:
    f.write(res.content)
