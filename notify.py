import requests
import json


def send_message(touser: str, content: str):
    # 保存要发送人员的账号,在通讯录可获取，多个人员之间使用空格分隔，以下为展示数据
    # 企业微信ID:企业微信管理界面-’我的企业‘页面中获取
    corpid = "ww1bee223ee201f1da"
    # 应用秘钥:在‘自建应用’-‘创建应用’-‘应用管理’中获取
    corpsecret = "v-XXmCJz_ZcS6Om661Ea8zARO4scd8kY9BZAeZ_2vnM"
    # 企业应用ID:在'自建应用'-'创建应用'-'应用管理'中获取
    agentid = 1000002

    # ------------------------以上变量需要自行修改-----------------------------------

    # 保存信息内容变量
    # curl -s 静默模式，就是不显示错误和进度
    baseurl = 'https://qyapi.weixin.qq.com/cgi-bin'
    req = requests.get(
        '{0}/gettoken?corpid={1}&corpsecret={2}'.format(baseurl, corpid, corpsecret))
    token = json.loads(req.text)['access_token']
    data = {
        "touser": touser,
        "msgtype": "text",
        "agentid": agentid,
        "text": {
            "content": content
        },
        "safe": 0
    }
    req = requests.post(
        '{0}/message/send?access_token={1}'.format(baseurl, token), data=json.dumps(data))
