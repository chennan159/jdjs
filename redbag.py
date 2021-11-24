"""
const $ = new Env("统计东哥历史红包");
统计东哥历史红包

"""
cookies = ''
redbag = ['Your JD_User', '买买买']

try:
    import requests
except Exception as e:
    print(e, "\n缺少requests 模块，请执行命令安装：python3 -m pip install requests")
    exit(3)
from urllib.parse import unquote
import sys
import re
import time
import os

pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep

## 获取通知服务
class msg(object):
    def __init__(self, m):
        self.str_msg = m
        self.message()
    def message(self):
        global msg_info
        print(self.str_msg)
        try:
            msg_info = "{}\n{}".format(msg_info, self.str_msg)
        except:
            msg_info = "{}".format(self.str_msg)
        sys.stdout.flush()
    def getsendNotify(self, a=0):
        if a == 0:
            a += 1
        try:
            url = 'https://gitee.com/curtinlv/Public/raw/master/sendNotify.py'
            response = requests.get(url)
            if 'curtinlv' in response.text:
                with open('sendNotify.py', "w+", encoding="utf-8") as f:
                    f.write(response.text)
            else:
                if a < 5:
                    a += 1
                    return self.getsendNotify(a)
                else:
                    pass
        except:
            if a < 5:
                a += 1
                return self.getsendNotify(a)
            else:
                pass
    def main(self):
        global send
        cur_path = os.path.abspath(os.path.dirname(__file__))
        sys.path.append(cur_path)
        if os.path.exists(cur_path + "/sendNotify.py"):
            try:
                from sendNotify import send
            except:
                self.getsendNotify()
                try:
                    from sendNotify import send
                except:
                    print("加载通知服务失败~")
        else:
            self.getsendNotify()
            try:
                from sendNotify import send
            except:
                print("加载通知服务失败~")
        ###################
msg("").main()
##############
def getEnvs(label):
    try:
        if label == 'True' or label == 'yes' or label == 'true' or label == 'Yes':
            return True
        elif label == 'False' or label == 'no' or label == 'false' or label == 'No':
            return False
    except Exception as e:
        pass
    try:
        if '.' in label:
            return float(label)
        elif '&' in label:
            return label.split('&')
        elif '@' in label:
            return label.split('@')
        else:
            return int(label)
    except:
        return label
class getJDCookie(object):
    # 适配各种平台环境ck

    def getckfile(self):
        global v4f
        curf = pwd + 'JDCookies.txt'
        v4f = '/jd/config/config.sh'
        ql_new = '/ql/config/env.sh'
        ql_old = '/ql/config/cookie.sh'
        if os.path.exists(curf):
            with open(curf, "r", encoding="utf-8") as f:
                cks = f.read()
                f.close()
            r = re.compile(r"pt_key=.*?pt_pin=.*?;", re.M | re.S | re.I)
            cks = r.findall(cks)
            if len(cks) > 0:
                return curf
            else:
                pass
        if os.path.exists(ql_new):
            print("当前环境青龙面板新版")
            return ql_new
        elif os.path.exists(ql_old):
            print("当前环境青龙面板旧版")
            return ql_old
        elif os.path.exists(v4f):
            print("当前环境V4")
            return v4f
        return curf

    # 获取cookie
    def getCookie(self):
        global cookies
        ckfile = self.getckfile()
        try:
            if os.path.exists(ckfile):
                with open(ckfile, "r", encoding="utf-8") as f:
                    cks = f.read()
                    f.close()
                if 'pt_key=' in cks and 'pt_pin=' in cks:
                    r = re.compile(r"pt_key=.*?pt_pin=.*?;", re.M | re.S | re.I)
                    cks = r.findall(cks)
                    if len(cks) > 0:
                        if 'JDCookies.txt' in ckfile:
                            print("当前获取使用 JDCookies.txt 的cookie")
                        cookies = ''
                        for i in cks:
                            if 'pt_key=xxxx' in i:
                                pass
                            else:
                                cookies += i
                        return
            else:
                with open(pwd + 'JDCookies.txt', "w", encoding="utf-8") as f:
                    cks = "#多账号换行，以下示例：（通过正则获取此文件的ck，理论上可以自定义名字标记ck，也可以随意摆放ck）\n账号1【Curtinlv】cookie1;\n账号2【TopStyle】cookie2;"
                    f.write(cks)
                    f.close()
            if "JD_COOKIE" in os.environ:
                if len(os.environ["JD_COOKIE"]) > 10:
                    cookies = os.environ["JD_COOKIE"]
                    print("已获取并使用Env环境 Cookie")
        except Exception as e:
            print(f"【getCookie Error】{e}")

        # 检测cookie格式是否正确
    def getUserInfo(self, ck, pinName, userNum):
        url = 'https://me-api.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New&callSource=mainorder&channel=4&isHomewhite=0&sceneval=2&sceneval=2&callback='
        headers = {
            'Cookie': ck,
            'Accept': '*/*',
            'Connection': 'close',
            'Referer': 'https://home.m.jd.com/myJd/home.action',
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'me-api.jd.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Mobile/15E148 Safari/604.1',
            'Accept-Language': 'zh-cn'
        }
        try:
            if sys.platform == 'ios':
                resp = requests.get(url=url, verify=False, headers=headers, timeout=60).json()
            else:
                resp = requests.get(url=url, headers=headers, timeout=60).json()
            if resp['retcode'] == "0":
                nickname = resp['data']['userInfo']['baseInfo']['nickname']
                return ck, nickname
            else:
                context = f"账号{userNum}【{pinName}】Cookie 已失效！请重新获取。"
                print(context)
                return ck, False
        except Exception:
            context = f"账号{userNum}【{pinName}】Cookie 已失效！请重新获取。"
            print(context)
            return ck, False

    def iscookie(self):
        """
        :return: cookiesList,userNameList,pinNameList
        """
        cookiesList = []
        userNameList = []
        pinNameList = []
        if 'pt_key=' in cookies and 'pt_pin=' in cookies:
            r = re.compile(r"pt_key=.*?pt_pin=.*?;", re.M | re.S | re.I)
            result = r.findall(cookies)
            if len(result) >= 1:
                print("您已配置{}个账号".format(len(result)))
                u = 1
                for i in result:
                    r = re.compile(r"pt_pin=(.*?);")
                    pinName = r.findall(i)
                    pinName = unquote(pinName[0])
                    # 获取账号名
                    ck, nickname = self.getUserInfo(i, pinName, u)
                    if nickname != False:
                        cookiesList.append(ck)
                        userNameList.append(nickname)
                        pinNameList.append(pinName)
                    else:
                        u += 1
                        continue
                    u += 1
                if len(cookiesList) > 0 and len(userNameList) > 0:
                    return cookiesList, userNameList, pinNameList
                else:
                    print("没有可用Cookie，已退出")
                    exit(3)
            else:
                print("cookie 格式错误！...本次操作已退出")
                exit(4)
        else:
            print("cookie 格式错误！...本次操作已退出")
            exit(4)
getCk = getJDCookie()
getCk.getCookie()
# 获取v4环境 特殊处理
if os.path.exists(v4f):
    try:
        with open(v4f, 'r', encoding='utf-8') as f:
            curenv = locals()
            for i in f.readlines():
                r = re.compile(r'^export\s(.*?)=[\'\"]?([\w\.\-@#!&=_,\[\]\{\}\(\)]{1,})+[\'\"]{0,1}$', re.M | re.S | re.I)
                r = r.findall(i)
                if len(r) > 0:
                    for i in r:
                        if i[0] != 'JD_COOKIE':
                            curenv[i[0]] = getEnvs(i[1])
    except:
        pass

if "redbag" in os.environ:
    if len(os.environ["redbag"]) > 1:
        redbag = os.environ["redbag"]
        redbag = redbag.replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(',')
        print("已获取并使用Env环境 redbag:", redbag)

def gettimestamp():
    return str(int(time.time() * 1000))


def printf(text):
    print(text)
    sys.stdout.flush()


def getinfo(ck):
    isNext = True
    page = 1
    sum = 0
    usedsum = 0
    jxsum = 0
    usedjx = 0
    litesum = 0
    usedlite = 0
    healthsum = 0
    usedhealth = 0
    jdsum = 0
    usedjd = 0
    tysum = 0
    usedty = 0
    count = 0
    while isNext:
        url = "https://wq.jd.com/user/info/QueryUserRedEnvelopesV2?type=2&orgFlag=JD_PinGou_New&page=%s&cashRedType=1&redBalanceFlag=0&channel=3&_=%s&sceneval=2&g_login_type=1&g_ty=ls" % (
            page, gettimestamp())
        headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'dnt': '1',
            'referer': 'https://wqs.jd.com/',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'cookie': 'pt_key=app_openAAJhnXFIADCKpIFQjR5KSKnYDArAxrOp6bbm3A1BbUH19_x0j4_yjAzJDRJUGA5DEOTithr5zzE;pt_pin=jd_7b64b6420dd31;'
        }
        r = requests.get(url, headers=headers).json()
        if r['data']['unUseRedInfo']['redList'] == None:
            print('最近六个月累计红包总数', count, '累计红包总额 %.2f' % sum, '已使用红包总额 %.2f' % usedsum)
            print(
                '\n其中：\n京东商城：总金额%.2f 已使用：%.2f\n京喜：总金额%.2f 已使用：%.2f\n极速版：总金额%.2f 已使用：%.2f\n京东健康：总金额%.2f 已使用：%.2f\n通用红包：总金额%.2f 已使用：%.2f\n' % (
                jdsum, usedjd, jxsum, usedjx, litesum, usedlite, healthsum, usedhealth, tysum, usedty))
            isNext = False
        else:
            page += 1
            count = r['data']['unUseRedInfo']['count']
            for i in r['data']['unUseRedInfo']['redList']:
                sum += float(i['discount'])
                usedsum += (float(i['discount']) - float(i['balance']))
                if "京喜" in i['orgLimitStr']:
                    jxsum += float(i['discount'])
                    usedjx += (float(i['discount']) - float(i['balance']))
                elif "极速" in i['orgLimitStr']:
                    litesum += float(i['discount'])
                    usedlite += (float(i['discount']) - float(i['balance']))
                elif "健康" in i['orgLimitStr']:
                    healthsum += float(i['discount'])
                    usedhealth += (float(i['discount']) - float(i['balance']))
                elif "京东商城" in i['orgLimitStr']:
                    jdsum += float(i['discount'])
                    usedjd += (float(i['discount']) - float(i['balance']))
                else:
                    tysum += float(i['discount'])
                    usedty += (float(i['discount']) - float(i['balance']))
