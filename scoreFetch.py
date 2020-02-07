# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import base64
'''
    查询成绩小程序，下方填写账号密码即可一键查询
    使用前务必先安装好必要的python包
'''

UserId = "2018030402055"  # 你的账号/学号
PassWd = "xxx"  # 你的密码


class Spider:
    login_url = 'http://jwgln.zsc.edu.cn/jsxsd/xk/LoginToXk'
    score_url = 'http://jwgln.zsc.edu.cn/jsxsd/kscj/cjcx_list'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/61.0.3163.100 Safari/537.36',
        'Host': 'jwgln.zsc.edu.cn',
        'Referer': 'http://jwgln.zsc.edu.cn/jsxsd/'
    }

    post_data = {

    }

    def login(self, user_id, pass_wd):
        encodes = str(base64.b64encode(bytes(user_id, 'utf-8')), 'utf-8') \
                  + '%%%' \
                  + str(base64.b64encode(bytes(pass_wd, 'utf-8')), 'utf-8')
        self.post_data['encoded'] = str(encodes)
        r_session = requests.session()
        r_session.post(self.login_url, headers=self.header, data=self.post_data)
        return r_session

    def get_page(self, r_session):
        response = r_session.get(self.score_url, headers=self.header)
        # print(response.text)
        text = response.text
        login_status = False
        if re.match(re.compile('.*请先登录系统.*', re.S), text) is None:
            login_status = True
        print(login_status)
        #print(text)
        return login_status, text

    def parse_page(self, page):
        b_soup = BeautifulSoup(page, 'lxml')
        raw_form = b_soup.find_all('tr')
        n = 1
        list = []
        for raw_row in raw_form:
            if n != 3:
                n += 1
                continue
            one_row = raw_row.find_all('td')
            smalllist = []
            for data in one_row:
                if len(str(data.string).strip()) == 0:
                    # print("None", end=' |')
                    smalllist.append(str("None"))
                else:
                    #print(str(data.string).strip(), end=' |')
                    smalllist.append(str(data.string))

            list.append(smalllist)
            #print('')

            #print('-' * 50)
        return list


def main():
    spider = Spider()
    login_session = spider.login(UserId, PassWd)
    status, page = spider.get_page(login_session)
    if not status:
        print('login error')
        #print(page)
        return
    list = spider.parse_page(page)
    print(list)


if __name__ == '__main__':
    main()
