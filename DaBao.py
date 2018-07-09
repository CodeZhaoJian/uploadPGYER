#!/usr/bin/python
#!/usr/bin/env python

#coding=utf-8 
import os
import commands
import requests
import webbrowser

import smtplib
from email.mime.text import MIMEText
'''
使用注意事项:该脚本基于python2.7
1、将工程的编译设备选成 Gemeric iOS Device
2、command + B编译
3、使用 终端 cd 至脚本文件存放目录 并执行 python DaBao.py 即可 （Mac 本身带有python2 环境，若安装了python3 环境请 执行 python3 DaBao.py）

⚠️⚠️⚠️ 发送方邮箱设置

邮件发送方式使用 SMTP服务 需设置SMTP服务

以QQ邮箱举例

QQ邮箱 -  设置  - 账户 - POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务 - IMAP/SMTP服务

在 “IMAP/SMTP服务” 右边会有一个 ”开启“ 按钮

点击开启按钮 会弹出一个对话框 里面有一个 16位的字符串 将此字符串 设置到下方 “mail_pass” 中 并将发送发QQ邮箱的地址填入 “mail_user”中
'''

appFileFullPath = '/Users/zhaojian/Library/Developer/Xcode/DerivedData/slazyiPhone-hdvbbhrsyjtuveemsuvhvofeinab/Build/Products/Debug-iphoneos/slazyiPhone.app'

PayLoadPath = '/Users/zhaojian/Desktop/Payload'
packBagPath = '/Users/zhaojian/Desktop/ProgramBag'

openUrlPath = 'xxxxxxxx'

downloadUrlPath = 'xxxxxxxxxx'

mail_user = '961826736@qq.com'                                 #发送方邮箱
mail_pass = 'xxxxxxxxx'                                   #填入发送方邮箱的授权码
mail_namelist = ["961826736@qq.com","33067321@qq.com"]  #收件人邮箱
#上传蒲公英
USER_KEY = "xxxxxxxxxxx"

API_KEY = "xxxxxxxxxxx"

#上传蒲公英
def uploadIPA(IPAPath):
    if(IPAPath==''):
        print "\n*************** 没有找到对应上传的IPA包 *********************\n"
        return
    else:
        print "\n***************开始上传到蒲公英*********************\n"
        url='http://www.pgyer.com/apiv1/app/upload'
        data={
            'uKey':USER_KEY,
            '_api_key':API_KEY,
            'installType':'2',
            'password':'',
            'updateDescription':des
        }
        files={'file':open(IPAPath,'rb')}
        r=requests.post(url,data=data,files=files)

def openDownloadUrl():
    webbrowser.open(openUrlPath)
    print "\n*************** 更新成功 *********************\n"

#编译打包流程
def bulidIPA():
    #打包之前先删除packBagPath下的文件夹
    commands.getoutput('rm -rf %s'%packBagPath)
    #创建PayLoad文件夹
    mkdir(PayLoadPath)
    #将app拷贝到PayLoadPath路径下
    commands.getoutput('cp -r %s %s'%(appFileFullPath,PayLoadPath))
    #在桌面上创建packBagPath的文件夹
    commands.getoutput('mkdir -p %s'%packBagPath)
    #将PayLoadPath文件夹拷贝到packBagPath文件夹下
    commands.getoutput('cp -r %s %s'%(PayLoadPath,packBagPath))
    #删除桌面的PayLoadPath文件夹
    commands.getoutput('rm -rf %s'%(PayLoadPath))
    #切换到当前目录
    os.chdir(packBagPath)
    #压缩packBagPath文件夹下的PayLoadPath文件夹夹
    commands.getoutput('zip -r ./Payload.zip .')
    print "\n*************** 打包成功 *********************\n"
    #将zip文件改名为ipa
    commands.getoutput('mv Payload.zip Payload.ipa')
    #删除payLoad文件夹
    commands.getoutput('rm -rf ./Payload')

#创建PayLoad文件夹
def mkdir(PayLoadPath):
    isExists = os.path.exists(PayLoadPath)
    if not isExists:
        os.makedirs(PayLoadPath)
        print PayLoadPath + '创建成功'
        return True
    else:
        print PayLoadPath + '目录已经存在'
        return False

#发送邮件
def send_qq_email(conen):
    try:
        #设置标题
        title = "App 测试版本更新"
        #设置内容       此内容拼接了 下载地址以及刚刚输入更新的日志描述
        content = "新版本已发布请前往:\n" + downloadUrlPath + " 下载测试" + "\n更新内容:" + conen
        
        msg = MIMEText(str(content))
        msg["Subject"] = title
        # 发件邮箱
        msg["From"] = mail_user
        #收件邮箱
        msg["To"] = ";".join(mail_namelist)
        # 设置服务器、端口
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        #登录邮箱
        s.login(mail_user, mail_pass)
        # 发送邮件
        s.sendmail(mail_user, mail_namelist, msg.as_string())
        s.quit()
        print "\n*************** 邮件发送成功! *********************\n"
        return True
    except smtplib.SMTPException:
        print "\n*************** 邮件发送失败! *********************\n"
        return False

if __name__ == '__main__':
    des = input("请输入更新的日志描述:")
    bulidIPA()
    uploadIPA('%s/Payload.ipa'%packBagPath)
    openDownloadUrl()
    send_qq_email(des)
