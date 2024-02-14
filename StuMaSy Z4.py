import requests
from bs4 import BeautifulSoup
from json import loads, dumps
from threading import Thread
from datetime import datetime
from pynput import keyboard
from os import listdir,execl
from sys import exit,executable,argv

# 全新Z4版本，无需修改代码直接运行
# 模块单导，速度更快！
def dq_yxcs(txtname):
    path2 = './Data/运行参数/' + txtname + '.txt'
    file2 = open(path2, 'r')
    content2 = file2.read()
    file2.close()
    return content2
def xr_yxcs(txtname,content):
    full_path = './Data/运行参数/' + txtname + '.txt'
    file = open(full_path, 'w')
    file.write(content)
    file.close()

print('欢迎您使用StuMaSy,初始化正在加载中...')
if dq_yxcs('账号') == '0':
    print('')
    print('检测到您的新用户,请填写以下信息')
    xr_yxcs('账号',input('请输入账号 : '))
    xr_yxcs('密码', input('请输入密码 : '))
    xr_yxcs('工作室ID', input('请输入工作室ID : '))
    print('接下来将填写自动同意用户进入工作室的条件')
    xr_yxcs('点赞条件', input('请输入点赞条件 / 个 : '))
    xr_yxcs('收藏条件', input('请输入收藏条件 / 个 : '))
    xr_yxcs('再创作条件', input('请输入再创作条件 / 个 : '))
    xr_yxcs('浏览量条件', input('请输入浏览量条件 / 个 : '))
    xr_yxcs('等级条件', input('请输入等级条件 / 1 无称号 2 潜力新星 3 进阶高手 4 编程大佬 5 源码传说 : '))
    print('按下可以ALT进入控制中心 输入 改参可以修改这些参数哦；还可以输入 生成积分排行榜 ')
    print('')
#账号
srzh = dq_yxcs('账号')
#密码
srmm = dq_yxcs('密码')
#工作室id
srgzsid = dq_yxcs('工作室ID')

# 申请加入工作室条件条件
# 点赞条件
dztj = dq_yxcs('点赞条件')
# 收藏条件
sctj = dq_yxcs('收藏条件')
# 浏览量条件
llltj = dq_yxcs('浏览量条件')
# 再创作条件
zcztj = dq_yxcs('再创作条件')
# 等级条件 1 无称号 2 潜力新星 3 进阶高手 4 编程大佬 5 源码传说
djtj = dq_yxcs('等级条件')

ua = 'User-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHtmL, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
gml = '.'
#读取工作室第二ID
czurl = 'https://api.codemao.cn/web/shops/' + str(srgzsid)
czr = requests.get(czurl)
czrj = czr.json()
ssgzsid = str(czrj['shop_id'])
tgsl = str(czrj['n_works'])
#其他数据
gzsname = czrj['name']
preview_url = czrj['preview_url']
description = czrj['description']

#替换最新的cookies
fxses = requests.session()
fxheaders = {"Content-Type": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
fxsoup = BeautifulSoup(requests.get('https://shequ.codemao.cn', headers=fxheaders).text, 'html.parser')
fxpid = loads(fxsoup.find_all("script")[0].string.split("=")[1])['pid']
fxa = fxses.post('https://api.codemao.cn/tiger/v3/web/accounts/login', headers=fxheaders,data=dumps({"identity": srzh, "password": srmm, "pid": fxpid}))
if fxa.status_code == 200:
    fxc = fxa.cookies
    fxcookies = requests.utils.dict_from_cookiejar(fxc)
    fxcookiess = 'authorization=' + fxcookies['authorization'] + ';acw_tc=' + fxcookies['acw_tc']
    src = fxcookiess
else:
    exit("不能登录编程猫")

#工作室评论
def gzspl():

    #修改
    def File_New(name, msg):
        desktop_path = gml + "/Data/" + \
            str(name)
        full_path = desktop_path + '.txt'
        file = open(full_path, 'w')
        file.write(msg)
        file.close()

    def File(e, a):
        desktop_path = gml +"/Data/用户积分存储文件夹/" + \
            str(e)
        full_path = desktop_path + '.txt'
        file = open(full_path, 'w')
        file.write(a)
        file.close()

    qdry = []
    #当前时间
    now_time = str(datetime.now().year) + '/' + str(datetime.now().month) + '/' + str(datetime.now().day)
    path1 = gml + '/Data/签到日期.txt'
    file1 = open(path1, 'r')
    content9 = file1.read()
    file1.close()
    if content9 == now_time:
        path1 = gml + '/Data/签到人员.txt'
        file1 = open(path1, 'r')
        contentx = file1.read()
        file1.close()
        qdry = contentx.split(',')
    else:
        full_path = gml + '/Data/签到日期.txt'
        file = open(full_path, 'w')
        file.write(now_time)
        file.close()
        full_path = gml + '/Data/签到人员.txt'
        file = open(full_path, 'w')
        file.write('0')
        file.close()
        qdry = [0]
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': ua,
            'Cookie': str(src)
        }
        url = 'https://api.codemao.cn/web/discussions/' + srgzsid + '/comment'
        data = {'content': "hallo，室员们，又是新的一天，输入全部指令即可查看全部指令哦", 'rich_content': "hallo，室员们，又是新的一天，输入全部指令即可查看全部指令哦", 'source': "WORK_SHOP"}
        do = requests.post(url=url,headers=headers,data=dumps(data))
        if do.status_code == 201:
            pass
        else:
            print('最初提示失败')
            print(do.json())
    #初始化+获取本地储存资料
    path1 = gml + '/Data/评论ID.txt'
    file1 = open(path1, 'r')
    content1 = file1.read()
    file1.close()
    zcx = content1.split(',')

    path2 = gml + '/Data/有积分用户.txt'
    file2 = open(path2, 'r')
    content2 = file2.read()
    file2.close()
    yjh = content2.split(',')


    #增加积分模块
    def pjf(idf,jf):
        if str(idf) in yjh:
            path3 = gml + '/Data/用户积分存储文件夹/' + \
                str(idf) + '.txt'
            file3 = open(path3, 'r')
            content3 = file3.read()
            content3 = int(content3)
            content3 += jf
            file3.close()
            File(str(idf), str(content3))
        else:
            content3 = str(content2) + ',' + str(idf)
            yjh.append(str(idf))
            File_New('有积分用户',content3)
            File(idf, str(5))

    print('初始化完毕，开始执行')

    while True:
        # 管理成员
        glry = []
        url = requests.get('https://api.codemao.cn/web/shops/' + srgzsid +'/users?limit=10&offset=0')
        url = url.json()['items']
        for i in range(0,len(url)):
            if url[i]['position'] == 'LEADER' or url[i]['position'] == 'DEPUTYLEADER':
                glry.append(str(url[i]['user_id']))
        #多次内嵌套循环
        for cs in range(0,5):
            #解析id/名称/评论的代码
            url = 'https://api.codemao.cn/web/discussions/' + srgzsid + '/comments'
            headers = {
                'User-Agent': ua
            }
            data = {
                'source': 'WORK_SHOP',
                'sort': '-created_at',
                'limit': '5',
                'offset': '0'
            }
            r = requests.get(url=url,headers=headers,params=data)
            data = r.json()
            items = data['items']
            items = items[cs]
            user = items['user']
            ida = items['id']               #评论ID 
            nickname = user['nickname']     #用户名字
            content = str(items['content'])      #评论内容
            yhid = user['id']               #用户ID

            #函数
            def zdhf(ifs,contents,inpu):
                if ida not in zcx:
                    if content == ifs:
                        ses = requests.session()
                        headers = {"Content-Type": "application/json","User-Agent": ua}
                        soup = BeautifulSoup(requests.get('https://shequ.codemao.cn', headers=headers).text, 'html.parser')
                        pid = loads(soup.find_all("script")[0].string.split("=")[1])['pid']
                        a = ses.post('https://api.codemao.cn/tiger/v3/web/accounts/login', headers=headers,data=dumps({"identity": srzh, "password": srmm, "pid": pid}))
                        if a.status_code == 200:
                            pass
                        else:
                            exit("抱歉,无法登录编程猫")
                        url2 = 'https://api.codemao.cn/web/discussions/' + srgzsid + '/comments/' + \
                        str(ida) + '/reply'
                        a = ses.post(url=url2, headers=headers, data=dumps(
                        {'parent_id': 0, 'content': contents, 'source': "WORK_SHOP"}))
                        if a.status_code == 201:
                            print('用户名为' + ' ' + str(nickname) + ' ' + str(inpu) + '(本次管理成功)')
                        else:
                            print("管理失败,请求出现问题")
                            print('服务器返回的问题原因 : ' + a.json()['error_message'])
                            print('正在启用PTS修复系统')
                            sfcg = 0
                            for i in range(100):
                                ses = requests.session()
                                headers = {
                                    "Content-Type": "application/json", "User-Agent": ua}
                                soup = BeautifulSoup(requests.get(
                                    'https://shequ.codemao.cn', headers=headers).text, 'html.parser')
                                pid = loads(soup.find_all("script")[
                                            0].string.split("=")[1])['pid']
                                a = ses.post('https://api.codemao.cn/tiger/v3/web/accounts/login',
                                            headers=headers, data=dumps({"identity": srzh, "password": srmm, "pid": pid}))
                                if a.status_code == 200:
                                    pass
                                else:
                                    exit("抱歉,无法登录编程猫")
                                url2 = 'https://api.codemao.cn/web/discussions/' + srgzsid + '/comments/' + \
                                    str(ida) + '/reply'
                                a = ses.post(url=url2, headers=headers, data=dumps(
                                    {'parent_id': 0, 'content': contents, 'source': "WORK_SHOP"}))
                                if a.status_code == 201:
                                    print('修复成功')
                                    sfcg = 1
                                    break
                            if sfcg == 1:
                                pass
                            else:
                                print('PTS修复失败，请联系管理员')

            #删除投稿
            if ida not in zcx:
                if len(content) > 4:
                    if content[0] + content[1] + content[2] + content[3] + content[4] == '删除投稿为':
                        ses = requests.session()
                        headers = {"Content-Type": "application/json","User-Agent": ua}
                        soup = BeautifulSoup(requests.get('https://shequ.codemao.cn', headers=headers).text, 'html.parser')
                        pid = loads(soup.find_all("script")[0].string.split("=")[1])['pid']
                        a = ses.post('https://api.codemao.cn/tiger/v3/web/accounts/login', headers=headers,data=dumps({"identity": srzh, "password": srmm, "pid": pid}))
                        if a.status_code == 200:
                            pass
                        else:
                            exit("抱歉,无法登录编程猫")
                        url2 = 'https://api.codemao.cn/web/discussions/' + srgzsid + '/comments/' + str(ida) + '/reply'
                        zpid = (content[5:len(content)])
                        urlngm = 'https://api.codemao.cn/creation-tools/v1/works/' + str(zpid)
                        xx = requests.get(urlngm)
                        if xx.status_code == 200:
                            xxjos = xx.json()
                            user_info = xxjos['user_info']
                            idid = user_info['id']
                            headers114514 = {
                                "Content-Type": "application/json;charset=UTF-8",
                                "User-Agent": ua,
                                'cookie': str(src)
                            }
                            data114514 = {
                                'id': ssgzsid,
                                'work_id': '168716906'
                            }
                            url = 'https://api.codemao.cn/web/work_shops/works/remove?id=' + ssgzsid + '&work_id=' + str(zpid)
                            p = requests.post(url=url,headers=headers114514, data=dumps({'id': ssgzsid, 'work_id': str(zpid)}))
                            if str(idid) == str(yhid) or yhid in glry:
                                if p.status_code == 200:
                                    a = ses.post(url=url2, headers=headers, data=dumps({'parent_id': 0, 'content': '作品删除成功！', 'source': "WORK_SHOP"}))
                                    if a.status_code == 201:
                                        print('用户名为' + ' ' + str(nickname) + ' ' + '删除了投稿' + '(本次管理成功)')
                                    else:
                                        print('服务器返回的问题原因 : ' + a.json()['error_message'])
                                        print('正在启用PTS修复系统')
                                        sfcg = 0
                                        for i in range(100):
                                            a = ses.post(url=url2, headers=headers, data=dumps(
                                                {'parent_id': 0, 'content': '作品删除成功！', 'source': "WORK_SHOP"}))
                                            if a.status_code == 201:
                                                print('修复成功')
                                                sfcg = 1
                                                break
                                        if sfcg == 0:
                                            print('PTS修复失败，请联系管理员')

                                else:
                                    a = ses.post(url=url2, headers=headers, data=dumps({'parent_id': 0, 'content': '删除错误(请检查是否打错ID))', 'source': "WORK_SHOP"}))
                                    print('用户名为' + ' ' + str(nickname) + ' ' + '删除投稿失败' + '(本次失败成功)')
                            else:
                                a = ses.post(url=url2, headers=headers, data=dumps(
                                    {'parent_id': 0, 'content': '非作者删投稿，想进黑名单是吧[doge]', 'source': "WORK_SHOP"}))
                                if a.status_code == 201:
                                    print('用户名为' + ' ' + str(nickname) +' ' + '非作者删投稿，想进黑名单是吧[doge]' + '(本次管理成功)')
                                else:
                                    print("管理失败,请求出现问题")
                                    print('服务器返回的问题原因 : ' + a.json()['error_message'])
                                    print('正在启用PTS修复系统')
                                    sfcg = 0
                                    for i in range(100):
                                        a = ses.post(url=url2, headers=headers, data=dumps({'parent_id': 0, 'content': '非作者删投稿，想进黑名单是吧[doge]', 'source': "WORK_SHOP"}))
                                        if a.status_code == 201:
                                            print('修复成功')
                                            sfcg = 1
                                            break
                                    if sfcg == 0:
                                        print('PTS修复失败，请联系管理员')

            #签到
            if ida not in zcx:
                if content == '签到':
                    ses = requests.session()
                    headers = {"Content-Type": "application/json","User-Agent": ua}
                    soup = BeautifulSoup(requests.get('https://shequ.codemao.cn', headers=headers).text, 'html.parser')
                    pid = loads(soup.find_all("script")[0].string.split("=")[1])['pid']
                    a = ses.post('https://api.codemao.cn/tiger/v3/web/accounts/login', headers=headers,data=dumps({"identity": srzh, "password": srmm, "pid": pid}))
                    if a.status_code == 200:
                        pass
                    else:
                        exit("抱歉,无法登录编程猫")
                    if yhid not in qdry:
                        url2 = 'https://api.codemao.cn/web/discussions/' + srgzsid + '/comments/' + str(ida) + '/reply'
                        a = ses.post(url=url2, headers=headers, data=dumps({'parent_id': 0, 'content': '签到成功 +5积分', 'source': "WORK_SHOP"}))
                        if a.status_code == 201:
                            print('用户名为' + ' ' + str(nickname) + ' ' + '成功签到' + '(本次管理成功)')
                            pjf(yhid,5)
                            qdry.append(yhid)
                            path1 = gml + '/Data/签到人员.txt'
                            file1 = open(path1, 'r')
                            contentT = file1.read()
                            file1.close()
                            full_path = gml + '/Data/签到人员.txt'
                            file = open(full_path, 'w')
                            file.write(str(contentT) + ',' + str(yhid))
                            file.close()
                        else:
                            print("管理失败,请求出现问题")
                            print('服务器返回的问题原因 : ' + a.json()['error_message'])
                            print('正在启用PTS修复系统')
                            sfcg = 0
                            for i in range(100):
                                a = ses.post(url=url2, headers=headers, data=dumps({'parent_id': 0, 'content': '签到成功 +5积分', 'source': "WORK_SHOP"}))
                                if a.status_code == 201:
                                    print('修复成功')
                                    sfcg = 1
                                    break
                            if sfcg == 0:
                                print('PTS修复失败，请联系管理员')
                    else:
                        url2 = 'https://api.codemao.cn/web/discussions/' + \
                            srgzsid + '/comments/' + str(ida) + '/reply'
                        a = ses.post(url=url2, headers=headers, data=dumps(
                            {'parent_id': 0, 'content': '今天已经签过到了哦', 'source': "WORK_SHOP"}))
                        if a.status_code == 201:
                            print('用户名为' + ' ' + str(nickname) +
                                  ' ' + '重复签到已拒签' + '(本次管理成功)')
                        else:
                            print("管理失败,请求出现问题")
                            print('服务器返回的问题原因 : ' + a.json()['error_message'])
                            print('正在启用PTS修复系统')
                            sfcg = 0
                            for i in range(100):
                                a = ses.post(url=url2, headers=headers, data=dumps(
                                    {'parent_id': 0, 'content': '今天已经签过到了哦', 'source': "WORK_SHOP"}))
                                if a.status_code == 201:
                                    print('修复成功')
                                    sfcg = 1
                                    break
                            if sfcg == 0:
                                print('PTS修复失败，请联系管理员')

            #查询积分
            if ida not in zcx:
                if content == '查询积分':
                    ses = requests.session()
                    headers = {"Content-Type": "application/json",
                            "User-Agent": ua}
                    soup = BeautifulSoup(requests.get(
                        'https://shequ.codemao.cn', headers=headers).text, 'html.parser')
                    pid = loads(soup.find_all("script")[0].string.split("=")[1])['pid']
                    a = ses.post('https://api.codemao.cn/tiger/v3/web/accounts/login', headers=headers,
                                data=dumps({"identity": srzh, "password": srmm, "pid": pid}))
                    if a.status_code == 200:
                        pass
                    else:
                        exit("抱歉,无法登录编程猫")
                    url2 = 'https://api.codemao.cn/web/discussions/' + srgzsid + '/comments/' + \
                        str(ida) + '/reply'
                    if yhid in yjh:
                        path4 = str(gml) + '/Data/用户积分存储文件夹/' + str(yhid) + '.txt'
                        file4 = open(path4, 'r')
                        content4 = file4.read()
                        jc = '查询成功，您的积分是：' + str(content4)
                        a = ses.post(url=url2, headers=headers, data=dumps({'parent_id': 0, 'content': jc, 'source': "WORK_SHOP"}))
                        if a.status_code == 201:
                            print('用户名为' + ' ' + str(nickname) + ' ' + '查询了积分' + '(本次管理成功)')
                        else:
                            print("管理失败,请求出现问题")
                            print('服务器返回的问题原因 : ' + a.json()['error_message'])
                            print('正在启用PTS修复系统')
                            sfcg = 0
                            for i in range(100):
                                a = ses.post(url=url2, headers=headers, data=dumps({'parent_id': 0, 'content': jc, 'source': "WORK_SHOP"}))
                                if a.status_code == 201:
                                    print('修复成功')
                                    sfcg = 1
                                    break
                            if sfcg == 0:
                                print('PTS修复失败，请联系管理员')
                    else:
                        url2 = 'https://api.codemao.cn/web/discussions/' + srgzsid + '/comments/' + str(ida) + '/reply'
                        a = ses.post(url=url2, headers=headers, data=dumps({'parent_id': 0, 'content': '您还没有积分哦', 'source': "WORK_SHOP"}))
                        if a.status_code == 201:
                            print('用户名为' + ' ' + str(nickname) + ' ' + '查询了积分' + '(本次管理成功)')
                        else:
                            print("管理失败,请求出现问题")
                            print('服务器返回的问题原因 : ' + a.json()['error_message'])
                            print('正在启用PTS修复系统')
                            sfcg = 0
                            for i in range(100):
                                a = ses.post(url=url2, headers=headers, data=dumps({'parent_id': 0, 'content': '您还没有积分哦', 'source': "WORK_SHOP"}))
                                if a.status_code == 201:
                                    print('修复成功')
                                    sfcg = 1
                                    break
                            if sfcg == 0:
                                print('PTS修复失败，请联系管理员')
            #删除全部投稿
            if ida not in zcx:
                if content == '删除我的全部投稿':
                    headers = {
                        'Content-Type': 'application/json;charset=UTF-8',
                        'User-Agent': ua,
                        'Cookie': str(src)
                    }
                    yyds = 0
                    cwcs = 0
                    for u in range(int(tgsl) // 20 + 1):
                        url = requests.get('https://api.codemao.cn/web/works/subjects/' + srgzsid + '/works?&offset=' + str(yyds) + '&limit=20&sort=-created_at,-id&user_id=1258391425&work_subject_id=' + srgzsid)

                        yyds += 20
                        url = url.json()['items']
                        for ee in range(0,len(url)):
                            if url[ee]['user']['id'] == yhid:
                                zpid = url[ee]['id']
                                url6 = 'https://api.codemao.cn/web/work_shops/works/remove?id=' + ssgzsid + '&work_id=' + str(zpid)
                                p = requests.post(url=url6, headers=headers,data=dumps({'id': ssgzsid, 'work_id': str(zpid)}))
                                if p.status_code == 200:
                                    pass
                                else:
                                    cwcs += 1
                    url2 = 'https://api.codemao.cn/web/discussions/' + srgzsid + '/comments/' + str(ida) + '/reply'
                    if cwcs == 0:
                        ses = requests.session()
                        a = ses.post(url=url2, headers=headers, data=dumps(
                            {'parent_id': 0, 'content': '删除全部投稿成功', 'source': "WORK_SHOP"}))
                        if a.status_code == 201:
                            print('用户名为' + ' ' + str(
                                nickname) + ' ' + '删除全部投稿成功' + '(本次管理成功)')
                        else:
                            print("管理失败,请求出现问题")
                            print('服务器返回的问题原因 : ' + a.json()['error_message'])
                            print('正在启用PTS修复系统')
                            sfcg = 0
                            for i in range(100):
                                a = ses.post(url=url2, headers=headers, data=dumps(
                                    {'parent_id': 0, 'content': '删除全部投稿成功',
                                     'source': "WORK_SHOP"}))
                                if a.status_code == 201:
                                    print('修复成功')
                                    sfcg = 1
                                    break
                            if sfcg == 0:
                                print('PTS修复失败，请联系管理员')
                    else:
                        yj = '删除投稿成功，但失败了' + str(cwcs) + '次'
                        a = ses.post(url=url2, headers=headers, data=dumps(
                            {'parent_id': 0, 'content': yj, 'source': "WORK_SHOP"}))
                        if a.status_code == 201:
                            print('用户名为' + ' ' + str(
                                nickname) + ' ' + yj + '(本次管理成功)')
                        else:
                            print("管理失败,请求出现问题")
                            print('服务器返回的问题原因 : ' + a.json()['error_message'])
                            print('正在启用PTS修复系统')
                            sfcg = 0
                            for i in range(100):
                                a = ses.post(url=url2, headers=headers, data=dumps(
                                    {'parent_id': 0, 'content': yj,
                                     'source': "WORK_SHOP"}))
                                if a.status_code == 201:
                                    print('修复成功')
                                    sfcg = 1
                                    break
                            if sfcg == 0:
                                print('PTS修复失败，请联系管理员')
            #串门
            zdhf('串门','欢迎(^-^)','串门了')

            #自动化作者
            zdhf('作者是谁','作者是PXstate','询问作者是谁')

            #唱歌
            zdhf('唱歌','鸡你太美，啊啊欧耶，鸡你实在是太美，啊啊欧耶。(doge+bushi)','让机器唱歌')

            #全部指令
            zdhf('全部指令','功能1 : 签到','正在查询所有指令1')
            zdhf('全部指令','功能2 : 串门', '正在查询所有指令2')
            zdhf('全部指令','功能3 : 唱歌', '正在查询所有指令3')
            zdhf('全部指令','功能4 : 查询积分', '正在查询所有指令4')
            zdhf('全部指令','功能5 : 删除投稿 （格式为  删除投稿为（作品id） ）', '正在查询所有指令5')
            zdhf('全部指令','功能6 : 删除全部投稿 （机器检查较慢，请耐心等待）', '正在查询所有指令6')
            zdhf('全部指令','以后可能会开发新的功能的', '正在查询所有指令')

            #本地防重
            if ida not in zcx:
                zcx.append(ida)
                content1 = str(content1) + ',' + str(ida)
                File_New('评论ID', str(content1))

#自动同意加工作室申请
def jgs():
    while True:
        url6 = 'https://api.codemao.cn/web/work_shops/users/unaudited/list?offset=0&limit=40&id=' + ssgzsid
        data6 = {
            'offset': '0',
            'limit': '40',
            'id': ssgzsid
        }
        headers6 = {
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': ua,
            'Cookie': str(src)
        }
        s = requests.get(url=url6,params=data6,headers=headers6)
        if s.status_code == 200:
            sj6 = s.json()
            its = sj6['items']
            if len(its) >= 1:
                for yad in range(0,len(its)):
                    it = its[yad]
                    uid = it['user_id']
                    nicknamename = it['nickname']
                    j = requests.get(url='https://api.codemao.cn/creation-tools/v1/user/center/honor?user_id=' + str(uid))
                    j = j.json()
                    lll = j['view_times']
                    dzl = j['liked_total']
                    scl = j['collected_total']
                    zczl = j['re_created_total']
                    dj = j['author_level']
                    if lll >= llltj and dzl >= dztj and scl >= sctj and zczl >= zcztj and dj >= djtj:
                        twourl = 'https://api.codemao.cn/web/work_shops/users/audit'
                        yx = requests.post(url=twourl,data=dumps({'id': ssgzsid, 'user_id': str(uid), 'status': "ACCEPTED"}),headers=headers6)
                        if yx.status_code == 200:
                            print(str(nicknamename) + '加入了工作室')
                            headers = {
                                'Content-Type': 'application/json;charset=UTF-8',
                                'User-Agent': ua,
                                'Cookie': str(src)
                            }
                            url = 'https://api.codemao.cn/web/discussions/' + srgzsid + '/comment'
                            data = {'content': nicknamename + "欢迎加入工作室！",
                                    'rich_content': nicknamename + "欢迎加入工作室！",
                                    'source': "WORK_SHOP"}
                            do = requests.post(url=url, headers=headers, data=dumps(data))
                            if do.status_code == 201:
                                pass
                            else:
                                print('进入工作室欢迎失败')
                                print(do.json())
                        else:
                            print('失败错误')
                            print(yx.json())
                    else:
                        print(str(nicknamename) + '未达到进入工作室标准')
                        twourl = 'https://api.codemao.cn/web/work_shops/users/audit'
                        yx = requests.post(url=twourl,data=dumps({'id': ssgzsid, 'user_id': str(uid), 'status': "UNACCEPTED"}),headers=headers6)
        else:
            print('自动同意申请报错，可能是因为COOKIES原因，你更改了密码，还可能是你并非（副）室长')

#更新cookies
def cookies():
    while True:
        fxses = requests.session()
        fxheaders = {"Content-Type": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
        fxsoup = BeautifulSoup(requests.get('https://shequ.codemao.cn', headers=fxheaders).text, 'html.parser')
        fxpid = loads(fxsoup.find_all("script")[0].string.split("=")[1])['pid']
        fxa = fxses.post('https://api.codemao.cn/tiger/v3/web/accounts/login', headers=fxheaders,data=dumps({"identity": srzh, "password": srmm, "pid": fxpid}))
        if fxa.status_code == 200:
            fxc = fxa.cookies
            fxcookies = requests.utils.dict_from_cookiejar(fxc)
            fxcookiess = 'authorization=' + fxcookies['authorization'] + ';acw_tc=' + fxcookies['acw_tc']
            global src
            src = fxcookiess
        else:
            exit("不能登录编程猫")

def control_center():
    def on_press(key):
        if key == keyboard.Key.alt_l:
            print('')
            a = input('CONTROL CENTER - 控制中心 为您服务 请输入指令 : ')
            if a == '生成积分排行榜':
                idlb = []
                jifenlb = []
                path = './Data/用户积分存储文件夹'
                for file_name in listdir(path):
                    path1 = './Data/用户积分存储文件夹/' + file_name
                    file1 = open(path1, 'r')
                    jntm = file1.read()
                    file1.close()
                    idlb.append(file_name[0:len(file_name)-4])
                    jifenlb.append(int(jntm))
                for i in range(len(jifenlb)):
                    for n in range(0, len(jifenlb) - 1 - i):
                        if jifenlb[n] < jifenlb[n + 1]:
                            jifenlb[n],jifenlb[n + 1] = jifenlb[n + 1],jifenlb[n]
                            idlb[n], idlb[n + 1] = idlb[n + 1], idlb[n]
                cs114514 = 0
                for drid in idlb:
                    ccj = requests.get(
                        url='https://api.codemao.cn/creation-tools/v1/user/center/honor?user_id=' + str(drid))
                    ccj = ccj.json()
                    nickname = ccj['nickname']
                    print('第' + str(cs114514 + 1) + '名 ' + nickname + ' - ' + str(jifenlb[cs114514]) + ' 积分')
                    cs114514 += 1
                print('')
            elif a == '改参':
                print('1.账号 2.密码 3.工作室ID 4.点赞条件 5.浏览量条件 6.收藏条件 7.再创作条件 8.等级条件')
                a = int(input('请输入需要修改的参的编号 --->> '))
                if a == 1:
                    xr_yxcs('账号', input('请输入账号 : '))
                elif a == 2:
                    xr_yxcs('密码', input('请输入密码 : '))
                elif a == 3:
                    xr_yxcs('工作室ID', input('请输入工作室ID : '))
                elif a == 4:
                    xr_yxcs('点赞条件', input('请输入点赞条件 / 个 : '))
                elif a == 5:
                    xr_yxcs('浏览量条件', input('请输入浏览量条件 / 个 : '))
                elif a == 6:
                    xr_yxcs('收藏条件', input('请输入收藏条件 / 个 : '))
                elif a == 7:
                    xr_yxcs('再创作条件', input('请输入再创作条件 / 个 : '))
                elif a == 8:
                    xr_yxcs('等级条件',input('请输入等级条件 / 1 无称号 2 潜力新星 3 进阶高手 4 编程大佬 5 源码传说 : '))
                else:
                    print('序列错误')
                awa = input('重新运行程序才会生效，是否现在立刻重启? ( 回复是或否 )')
                if awa == '是':
                    # 获取当前解释器路径
                    p = executable
                    # 启动新程序(解释器路径, 当前程序)
                    execl(p, p, *argv)
                    # 关闭当前程序
                    exit()
                else:
                    print('')
            else:
                print('此指令无效')
    listener = keyboard.Listener(on_press=on_press)
    listener.start()


t1 = Thread(name='t1', target=gzspl)
t2 = Thread(name='t2', target=jgs)
t3 = Thread(name='t3', target=cookies)
t4 = Thread(name='t4', target=control_center)
t1.start()
t2.start()
t3.start()
t4.start()
