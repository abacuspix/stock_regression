# !/usr/bin/env python
# coding=utf-8
import smtplib
from email.mime.text import MIMEText
# 发送邮件
def sendMail(username,pwd,from_addr,to_addr,msg):
    try:
        smtp = smtplib.SMTP() 
        smtp.connect('smtp.163.com') 
        smtp.login(username, pwd) 
        smtp.sendmail(from_addr,to_addr, msg) 
        smtp.quit()
    except Exception as e:  
        print(str(e))
# 组织邮件        
message = MIMEText('Python 邮件发送测试', 'plain', 'utf-8')
message['Subject'] = 'Hello,用Python发送邮件'
sendMail('hsm_computer','xxx','hsm_computer@163.com','hsm_computer@163.com',message.as_string())    