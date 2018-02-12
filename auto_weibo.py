import os
import time
import MySQLdb
import urllib
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import SendKeys


driver = webdriver.Firefox()
driver.get("https://weibo.com/login.php")
driver.implicitly_wait(30)
# 登录微博
driver.find_element_by_id("loginname").clear()
driver.find_element_by_id("loginname").send_keys("")   # 输入用户名
driver.find_element_by_name("password").send_keys("")  # 输入密码
driver.find_element_by_css_selector(".W_btn_a.btn_32px").click()

WebDriverWait(driver,30,1).until(expected_conditions.title_contains(u"我的首页"))
time.sleep(15)


# 添加图片
if True:
  upload = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[3]/div[2]/div[1]/div[1]/div/div[3]/div[2]/a[2]")
  upload.click()
  img_path = "D:\\tmp\\images\\146040450.jpg"
  SendKeys.SendKeys(str(img_path))
  SendKeys.SendKeys("{ENTER}")
  SendKeys.SendKeys("{ENTER}")
  time.sleep(5) # 等待上传图片

# 发送微博
st = u"【淘宝发红包了，有机会拿最高2018元红包！点击链接：http://www.dwntme.com/h.Wtxvqhg " +\
     u"或复制这条信息￥icgW0nefUDh￥后打开手淘"
driver.find_element_by_css_selector("textarea.W_input").clear()
driver.find_element_by_css_selector("textarea.W_input").send_keys(st)
driver.implicitly_wait(3) # 加一下延时
driver.find_element_by_css_selector(".W_btn_a.btn_30px").click()
