#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import MySQLdb
import string
import urllib.request as urllib2
import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart  
from email import encoders
from email.header import Header
from email.mime.image import MIMEImage
'''
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
from email.MIMEImage import MIMEImage
from email.Encoders import encode_base64
'''
#设置服务器，用户名、口令以及邮箱的后缀
mail_host = ""
mail_user = ""
mail_pass = ""

#mysql 登录信息
db_host="localhost"
db_port=3306
db_user="root"
db_passwd=""
db_name="test"

msg = ""
send_succ = 0
send_fail = 0

# 获取推荐信息
def ConstructProduct():
  sql = 'select prd_name,prd_pig,voucher_url,voucher_name from test.recommend_list where channel = 0 limit 10'
  src_db = MySQLdb.connect(host=db_host,port=db_port,user=db_user,passwd=db_passwd,db=db_name,charset='utf8')
  cursor = src_db.cursor()
  cursor.execute(sql)
  results = cursor.fetchall()
  cursor.close()
  src_db.close()
  return results

# 组装邮件内容
def ConstructMsg():
  global msg
  subject = "天猫优惠购物"
  
  recommend_list = ConstructProduct()
  
  msg = MIMEMultipart('related')
  msg['From'] = mail_user
  msg['Subject'] = Header(subject, 'utf-8')
  
  msgAlternative = MIMEMultipart('alternative')
  msg.attach(msgAlternative)
  i = 0
  content = ''
  for row in recommend_list:
    content += '<p>' + row[0] + '<p><img src="cid:image' + str(i) +\
               '</img></p><p>可使用红包：' + row[3] + '<a href="' + row[2] + '">点击领取</a></p></p>'
    req = urllib2.Request(row[1])
    fd = urllib2.urlopen(req)
    imgbuf = bytearray()
    imgtype = row[1][row[1].rfind('.')+1:]
    while 1:
      data = fd.read(1024)
      if not len(data):
        break
      imgbuf.extend(data)
    msgImage = MIMEImage(bytes(imgbuf),imgtype)
    msgImage.add_header('Content-ID', '<image'+str(i)+'>')
    msg.attach(msgImage)
    i += 1
  print (content)
  msgAlternative.attach(MIMEText(content, 'html', 'utf-8'))

def ReportEmail():
  sql = "select distinct e_mail from test.t_email_info where e_type = 'qcyy'"
  src_db = MySQLdb.connect(host=db_host,port=db_port,user=db_user,passwd=db_passwd,db=db_name)
  cursor = src_db.cursor()
  cursor.execute(sql)
  results = cursor.fetchall()
  for row in results:
    mail_receiver = row[0]
    SendMail(msg,mail_receiver)
    time.sleep(5)
  cursor.close()
  src_db.close()

# 可使用测试发送给对方邮箱
def ReportEmailTest():
  mail_receiver = ""
  SendMail(msg,mail_receiver)

def SendMail(msg,mail_receiver):
  global send_succ
  global send_fail
  send_status = 1
  msg['To'] = mail_receiver
  try:
    mailServer = smtplib.SMTP()
    mailServer.connect(mail_host)
    mailServer.login(mail_user,mail_pass)
    mailServer.sendmail(mail_user, mail_receiver, msg.as_string())
    mailServer.close()
  except Exception as e:
    print (e)
    send_status = 0
  if send_status == 0:
    send_fail += 1
    print("%s send e_mail failed!" % mail_receiver)
    return False
  else:
    send_succ += 1
    print("%s send e_mail success!" % mail_receiver)
    return True

def main():
  ConstructMsg()
  #ReportEmail()
  ReportEmailTest()
  #print("send succ %d fail %d" % (send_succ, send_fail))

if __name__ == "__main__":
  main()
