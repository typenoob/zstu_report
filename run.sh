#! /bin/bash
source /etc/profile
cd /srv/zstu
count=0
stoped=5
result=`python3 main.py`
while [[ ! $result == "successful!" ]]    # 判断程序上次运行是否正常结束
do
    echo "Process exits with errors! Restarting!"
    if [ $count == $stoped ]
    then
        echo "Process exits with errors! Can't autofix!"
	break
    else
	count=`expr $count + 1`
    fi
    result=`python3 main.py`
done

#使用方法 sh ./send_message.sh "发送内容"
#如       sh ./send_message.sh "测试环境，正在更新"


#保存要发送人员的账号,在通讯录可获取，多个人员之间使用空格分隔，以下为展示数据
user="ChenYuTao"
#企业微信ID:企业微信管理界面-’我的企业‘页面中获取
corpid="ww1bee223ee201f1da"
#应用秘钥:在‘自建应用’-‘创建应用’-‘应用管理’中获取
corpsecret="v-XXmCJz_ZcS6Om661Ea8zARO4scd8kY9BZAeZ_2vnM"
#企业应用ID:在'自建应用'-'创建应用'-'应用管理'中获取
agentld=1000002

#------------------------以上变量需要自行修改-----------------------------------

#保存信息内容变量
#curl -s 静默模式，就是不显示错误和进度
A=`curl -s https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=$corpid\&corpsecret=$corpsecret`
#解析json格式 并获取access_token值
token=`echo $A | jq -c '.access_token'`
#去除变量值两边的双引号
token=${token#*\"}
token=${token%*\"}
#请求地址
URL="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=$token"


for I in $user;do
	#发送的JSON内容
	JSON="{\"touser\": \"$I\",\"msgtype\": \"text\",\"agentid\": \"$agentld\",\"text\": {\"content\": \"$result\"},\"safe\":0 }"
	#以POST的方式请求
	curl -d "$JSON" "$URL"
done

exit 0

#http://qydev.weixin.qq.com/wiki/index.php 企业号开发者中心
#text消息JSON格式如下：
#{
#   "touser": "UserID1|UserID2|UserID3",			成员ID列表，多个以|分隔，@all则向所有成员发送
#   "toparty": " PartyID1 | PartyID2 ",				部门ID列表
#   "totag": " TagID1 | TagID2 ",				标签ID列表
#   "msgtype": "text",						消息类型
#   "agentid": 1,						企业应用的id
#   "text": {							
#       "content": "Holiday Request For Pony(http://xxxxx)"	消息内容最长不超过2048个字节，微信提醒上显示20个字
#   },
#   "safe":0							表示是否是保密消息，0表示否，1表示是，默认0 
#}
