"""
const $ = new Env("统计东哥历史红包");
统计东哥历史红包

"""

import requests
import sys
import re
import time
import os


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


if __name__ == '__main__':
	ck='pt_key=app_openAAJhnXFIADCKpIFQjR5KSKnYDArAxrOp6bbm3A1BbUH19_x0j4_yjAzJDRJUGA5DEOTithr5zzE;pt_pin=jd_7b64b6420dd31;'
	
	getinfo(ck);