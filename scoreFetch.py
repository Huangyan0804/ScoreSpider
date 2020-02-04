# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
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

    keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

    def _encodeInp(self, inputs):
        i = 0
        output = ""
        while True:
            chr2 = chr3 = 0
            chr1 = ord(inputs[i])
            i += 1
            flag2 = False
            if i < len(inputs):
                chr2 = ord(inputs[i])
            else:
                flag2 = True
            i += 1
            flag3 = False
            if i < len(inputs):
                chr3 = ord(inputs[i])
            else:
                flag3 = True
            i += 1
            enc1 = chr1 >> 2
            enc2 = ((chr1 & 3) << 4) | (chr2 >> 4)
            enc3 = ((chr2 & 15) << 2) | (chr3 >> 6)
            enc4 = chr3 & 63
            if flag2:
                enc3 = enc4 = 64
            elif flag3:
                enc4 = 64
            output = output + self.keyStr[enc1] + self.keyStr[enc2] \
                + self.keyStr[enc3] + self.keyStr[enc4]
            if i >= len(inputs):
                break
        return output

    post_data = {

    }

    def login(self, user_id, pass_wd):
        encodes = self._encodeInp(user_id) + '%%%' + self._encodeInp(pass_wd)
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
