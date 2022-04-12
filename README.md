# E浙理自动健康申报（新版）
[![Publish Docker](https://github.com/typenoob/zstu_report/actions/workflows/publish_docker.yml/badge.svg)](https://github.com/typenoob/zstu_report/actions/workflows/publish_docker.yml)
![School](https://img.shields.io/badge/School-ZSTU-lightblue.svg)

**！请填写登录sso的学号和密码，不能是手机号。**

2021/12/29更新：基于docker构建，简化流程。
2022/4/11更新：通过github action持续构建docker镜像，确保可用性。

## 快速开始

### 自己构建镜像 

```
docker build -t zstu_report .
docker run zstu_report --rm --name zstu_report --restart=always -p 5000:5000
```

### 使用我上传的镜像

```
docker run typenoob/zstu_report --rm --name zstu_report --restart=always -p 5000:5000
```

