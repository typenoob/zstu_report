import datetime
import json
import logging
import time
from random import choice
from tokenize import Triple
from notify import send_message
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class HealthRep:
    def __init__(self, gui=False, chromedriver_logging=False) -> None:
        chrome_options = webdriver.ChromeOptions()
        if not chromedriver_logging:
            chrome_options.add_argument('--silent')
            chrome_options.add_argument("--log-level=3")

        if not gui:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
        self.__client = webdriver.Chrome(options=chrome_options)
        self.__wait = WebDriverWait(self.__client, 10, 0.5)
        self.__flag = False

    def __get_element_by_xpath(self, xpath: str):
        return self.__wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    def login(self, username: str, password: str) -> bool:
        self.__username = username
        self.__flag = False
        try:
            urls = \
                [
                    'http://fangyi.zstu.edu.cn:6006/iForm/1817056F47E744D3B8488B'
                ]
            self.__client.get(choice(urls))
            username_input = self.__get_element_by_xpath(
                '/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div[1]/app-login-normal/div/form/div[1]/nz-input-group/input')
            password_input = self.__get_element_by_xpath(
                '/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div[1]/app-login-normal/div/form/div[2]/nz-input-group/input')
            login_button = self.__get_element_by_xpath(
                '/html/body/app-root/app-right-root/rg-page-container/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div[1]/app-login-normal/div/form/div[6]/div/button')
            username_input.send_keys(username)
            password_input.send_keys(password)
            login_button.click()
        except Exception as e:
            print(e)
            return False
        else:
            return True

    def do(self, location: str, workflow: list) -> bool:
        try:
            self.__wait.until(EC.alert_is_present())
            alertObject = self.__client.switch_to.alert
            alertObject.accept()
            self.__get_element_by_xpath(
                '//*[@id="iform"]/div[1]/div[3]/form/div[4]/div/div/div[2]/div/div/div/div/div')
            self.__client.execute_script(
                'document.getElementsByClassName("van-field__control")[6].readOnly = false')
            detailed_area_input = self.__get_element_by_xpath(
                '//*[@id="iform"]/div[1]/div[3]/form/div[6]/div/div/div[2]/div/div/div/div[1]/input')
            detailed_area_input.clear()
            detailed_area_input.send_keys(location)
            # 因为数据有自动填充，所以这一段不需要了
            # workflow = \
            # [
            #     '//*[@id="iform"]/div[1]/div[3]/form/div[7]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span', # 低风险
            #     '//*[@id="iform"]/div[1]/div[3]/form/div[8]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span', # 在校内
            #     '//*[@id="iform"]/div[1]/div[3]/form/div[9]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span', # 健康状况
            #     '//*[@id="iform"]/div[1]/div[3]/form/div[10]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span', # 绿码
            #     '//*[@id="iform"]/div[1]/div[3]/form/div[11]/div/div/div[2]/div/div/div/div[1]/div/div[2]/span', # 已完成首轮全部
            #     '//*[@id="iform"]/div[1]/div[3]/form/div[12]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span', # 无密切接触
            #     '//*[@id="iform"]/div[1]/div[3]/form/div[16]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span', # 未隔离
            #     '//*[@id="iform"]/div[1]/div[3]/form/div[17]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span', # 无省外旅行史
            #     '//*[@id="iform"]/div[1]/div[3]/form/div[18]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span', # 家人无风险地区旅行史
            # ]
            # workflow = \
            #     [
            #         # 未进行核酸检测
            #         '//*[@id="iform"]/div[1]/div[3]/form/div[21]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span',
            #         # 未进行抗原检测
            #         '//*[@id="iform"]/div[1]/div[3]/form/div[22]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span',
            #         # 当前在校学习
            #         '//*[@id="iform"]/div[1]/div[3]/form/div[23]/div/div/div[2]/div/div/div/div[1]/div/div[1]/span',
            #     ]
            for work in workflow:
                self.__get_element_by_xpath(work).click()

            self.__get_element_by_xpath(
                '//*[@id="iform"]/div[1]/div[4]/div/button[1]').click()
            self.__get_element_by_xpath(
                '/html/body/div[3]/div[3]/button[2]').click()

            if not self.check():
                raise RuntimeError("E")

        except:
            return False
        else:
            self.__flag = True
            return True

    def check(self) -> bool:
        url = 'http://fangyi.zstu.edu.cn:5004/api/DataSource/GetDataSourceByNo?sqlNo=JTDK_XS${}'
        res = json.loads(requests.get(url.format(self.__username)).text)
        logging.info('Checking data:{}'.format(res))
        if len(res['data']) == 0:
            return False
        unix_dtime = int(time.mktime(datetime.date.today().timetuple()))
        unix_ctime = int(time.mktime(time.strptime(
            res['data'][0]['CURRENTDATE'], '%Y-%m-%d %H:%M:%S')))
        logging.info('unix_dtime: {}, unix_ctime:{}'.format(
            unix_dtime, unix_ctime))
        return True if unix_dtime <= unix_ctime else False

    def static_check(username: str) -> bool:
        url = 'http://fangyi.zstu.edu.cn:5004/api/DataSource/GetDataSourceByNo?sqlNo=JTDK_XS${}'
        res = json.loads(requests.get(url.format(username)).text)
        logging.info('Checking data:{}'.format(res))
        if len(res['data']) == 0:
            return False
        unix_dtime = int(time.mktime(datetime.date.today().timetuple()))
        unix_ctime = int(time.mktime(time.strptime(
            res['data'][0]['CURRENTDATE'], '%Y-%m-%d %H:%M:%S')))
        logging.info('unix_dtime: {}, unix_ctime:{}'.format(
            unix_dtime, unix_ctime))
        return True if unix_dtime <= unix_ctime else False

    def destruct(self):
        self.__client.quit()

    def status(self) -> bool:
        return self.__flag


def main(dev: bool = False):
    logging.basicConfig(level=logging.INFO, filename="daily.log", filemode="w",
                        format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    with open('./essentials.json', 'r', encoding='utf-8') as f:
        essentials = json.load(f)
        users = essentials['users']
        for user in users:
            retries = user.get('retries', 0)
            workflow = user.get('workflow', essentials['workflow'])
            hr = HealthRep(gui=True)
            if hr.login(user['username'], user['password']):
                if hr.check():
                    if dev:
                        return '已经打过卡了！'
                    logging.info(
                        'already_reported: {}'.format(user['username']))
                    if user['notify_id']:
                        send_message(user['notify_id'], '已经打过卡了！')
                else:
                    if dev:
                        return '打卡成功！'
                    while retries >= 0:
                        if hr.do(user['location'], workflow):
                            logging.info(
                                'succeed: {}'.format(user['username']))
                            if user['notify_id']:
                                send_message(user['notify_id'], '打卡成功！')
                            break
                        retries -= 1
                    else:
                        if dev:
                            return '打卡失败！'
                        logging.info('error: {}'.format(user['username']))
                        if user['notify_id']:
                            send_message(user['notify_id'], '打卡失败！')
                        if retries == 0:
                            break
            hr.destruct()


if __name__ == '__main__':
    main()
