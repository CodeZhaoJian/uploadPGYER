#!/usr/bin/env python
#coding=utf-8 
import os
import requests
import webbrowser
import subprocess
import shutil

import smtplib
from email.mime.text import MIMEText
'''
使用注意事项:该脚本基于python3.6
1、将工程的编译设备选成 Gemeric iOS Device
2、command + B编译
3、执行脚本文件

'''

appFileFullPath = '/Users/zhaojian/Library/Developer/Xcode/DerivedData/slazyiPhone-aheuceqholetgucxufwteytuaosi/Build/Products/Debug-iphoneos/slazyiPhone.app'

PayLoadPath = '/Users/zhaojian/Desktop/Payload'
packBagPath = '/Users/zhaojian/Desktop/ProgramBag'
openUrlPath = 'https://www.pgyer.com/manager/dashboard/app/81cd3abf546db122acbdf46c7122f372'
downloadUrlPath = 'https://www.pgyer.com/IrEO'

mail_user = ''                                 #发送方邮箱
mail_pass = ''                                   #填入发送方邮箱的授权码
msg_to = '961826736@qq.com'                                  #收件人邮箱
mail_namelist = ["961826736@qq.com","33067321@qq.com"]
#上传蒲公英
USER_KEY = ""
API_KEY = ""

#上传蒲公英
def uploadIPA(IPAPath):
    if(IPAPath==''):
        print ("\n*************** 没有找到对应上传的IPA包 *********************\n")
        return
    else:
        print ("\n***************开始上传到蒲公英*********************\n")
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
    print ("\n*************** 更新成功 *********************\n")

#编译打包流程
def bulidIPA():
    #删除之前打包的ProgramBag文件夹
    subprocess.call(["rm","-rf",packBagPath])
    #创建PayLoad文件夹
    mkdir(PayLoadPath)
    #将app拷贝到PayLoadPath路径下
    subprocess.call(["cp","-r",appFileFullPath,PayLoadPath])
    #在桌面上创建packBagPath的文件夹
    subprocess.call(["mkdir","-p",packBagPath])
    #将PayLoadPath文件夹拷贝到packBagPath文件夹下
    subprocess.call(["cp","-r",PayLoadPath,packBagPath])
    #删除桌面的PayLoadPath文件夹
    subprocess.call(["rm","-rf",PayLoadPath])
    #切换到当前目录
    os.chdir(packBagPath)
    #压缩packBagPath文件夹下的PayLoadPath文件夹夹
    subprocess.call(["zip","-r","./Payload.zip","."])
    print ("\n*************** 打包成功 *********************\n")
    #将zip文件改名为ipa
    subprocess.call(["mv","payload.zip","Payload.ipa"])
    #删除payLoad文件夹
    subprocess.call(["rm","-rf","./Payload"])


#创建PayLoad文件夹
def mkdir(PayLoadPath):
    isExists = os.path.exists(PayLoadPath)
    if not isExists:
        os.makedirs(PayLoadPath)
        print (PayLoadPath + '创建成功')
        return True
    else:
        print (PayLoadPath + '目录已经存在')
        return False

#发送邮件
def send_qq_email(title,conen):
    try:
        
        content = "新版本已发布请前往:\n" + downloadUrlPath + " 下载测试" + "\n更新内容:" + conen
        
        msg = MIMEText(str(content))
        #设置标题
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
        print ("\n*************** 邮件发送成功! *********************\n")
        return True
    except smtplib.SMTPException:
        print ("\n*************** 邮件发送失败! *********************\n")
        return False

if __name__ == '__main__':
    des = input("请输入更新的日志描述:")
    bulidIPA()
    uploadIPA('%s/Payload.ipa'%packBagPath)
    openDownloadUrl()
    send_qq_email("App 测试版本更新",des)
