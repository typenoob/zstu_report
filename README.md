# E浙理自动健康申报（新版）
[![Publish Docker](https://github.com/typenoob/zstu_report/actions/workflows/publish-docker.yml/badge.svg)](https://github.com/typenoob/zstu_report/actions/workflows/publish-docker.yml)
![School](https://img.shields.io/badge/School-ZSTU-lightblue.svg)

**！请填写登录sso的学号和密码，不能是手机号。**

2021/12/29更新：基于docker构建，简化流程。
2022/4/11更新：通过github action持续构建docker镜像，确保可用性。
2022/5/13更新：可用性修复。多用户支持。增加输入选项:当前位置、工作流、重试次数。改进推送方式。

## 快速开始

### 自己构建镜像 

```
docker build -t zstu_report .
docker run -d --name zstu_report --restart=always -p 5000:5000 zstu_report
```

### 使用我上传的镜像

```
docker run -d --name zstu_report --restart=always -p 5000:5000 typenoob/zstu_report
```

## 配置说明

配置文件为单一文件essentials.json

- username:你的学号
- password:你的密码
- location:你当前居住的城市（默认：浙江省 杭州市 钱塘区）
- notify_id:通知账号名称（默认：空，详见下文 通知账号获取）
- retries:失败后最大重试次数（默认：0）
- workflows:工作流（详见工作流获取方法）

## 工作流程

1. 进入打卡的web页面，自动跳转到sso登录页面
2. 输入用户名、密码并登录
3. 跳转到打卡页面，载入已保存的信息
4. 填入居住地
5. 执行工作流（详见工作流获取方法）
6. 失败后继续尝试n次
7. 执行下一个用户

## 通知账号获取

微信扫描下面二维码后

![image](https://user-images.githubusercontent.com/61347081/168256907-e0b86029-b1d5-4d58-840a-7c3a87640175.png)

将自己的企业微信账号名称填入notify_id字段

## 工作流获取

1. 进入[打卡网页](http://fangyi.zstu.edu.cn:6006/iForm/1817056F47E744D3B8488B)
2. 按下F12，打开控制台
3. 点击左上角的按钮进行元素审查，选中想要审查的元素
4. 选中的元素中将会在元素选项卡高亮标出，右键它选择复制->复制xpath
5. 将复制到的内容添加至workflows字段

## TODO

- 使用 `curl -x {ip}:{port} sso.zstu.edu.cn` 验证http代理服务器的可用性后，使用代理服务器进行打卡操作，防止国外机被学校屏蔽ip

