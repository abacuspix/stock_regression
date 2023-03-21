# !/usr/bin/env python
# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
HTMLContent = '<html><head></head><body>'\
 '<h1>Hello</h1>This is <a href="https://www.cnblogs.com/JavaArchitect/">My Blog.</a>'\
 '</body></html>'        
message = MIMEMultipart()
body = MIMEText(HTMLContent, 'html', 'utf-8')
message.attach(body)
message['Subject'] = 'Hello,用Python发送邮件'
message['From'] = 'hsm_computer@163.com'                # 邮件上显示的收件人
message['To'] ='hsm_computer@163.com,153086207@qq.com'  # 邮件上显示的发件人
file = MIMEText(open('D:\\stockData\\ch9\\6008862019-01-012019-05-31.csv', 'rb').read(),'plain', 'utf-8')
file['Content-Type'] = 'application/text'
file['Content-Disposition'] = 'attachment;filename="stockInfo.csv"'
message.attach(file)
sendMail('hsm_computer','xxx','hsm_computer@163.com',['hsm_computer@163.com', '153086207@qq.com'],message.as_string())    