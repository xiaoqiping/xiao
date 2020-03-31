# coding=utf-8
from datetime import datetime
import itchat
import xlrd
from apscheduler.schedulers.background import BlockingScheduler
import os
#
# 一、简介
# 1，使用微信，定时往指定的微信群里发送指定信息。
#
# 2，需要发送的内容使用excel进行维护，指定要发送的微信群名、时间、内容。
#
# 二、py库
# 1，itchat：这个是主要的工具，用于连接微信个人账号接口。以下是一些相关的知识点网站。
#
# 2，xlrd：这个是用来读Excel文件的工具。
#
# 3，apscheduler：这个是用来定时调度时间的工具。
#
# http://www.lovean.com/view-24-336493-0.html
#



def SentChatRoomsMsg(name, context):
  itchat.get_chatrooms(update=True)
  iRoom = itchat.search_chatrooms(name)
  for room in iRoom:
    if room['NickName'] == name:
      userName = room['UserName']
      break
  itchat.send_msg(context, userName)
  print("发送时间：" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
    "发送到：" + name + "\n"
    "发送内容：" + context + "\n")
  print("*********************************************************************************")
  scheduler.print_jobs()
def loginCallback():
  print("***登录成功***")
def exitCallback():
  print("***已退出***")
itchat.auto_login(hotReload=False, enableCmdQR=True, loginCallback=loginCallback, exitCallback=exitCallback)
#workbook = xlrd.open_workbook(os.path.join(os.path.dirname(os.path.realpath(__file__)), "chatroomsfile\AutoSentChatroom.xlsx"))
workbook = xlrd.open_workbook("D:\\xiao\www\\acquisition.szlcsc.com\\file\\微信\\AutoSentChatroom.xlsx")
sheet = workbook.sheet_by_name('Chatrooms')
iRows = sheet.nrows
scheduler = BlockingScheduler()
index = 1
for i in range(1, iRows):
  textList = sheet.row_values(i)
  name = textList[0]
  context = textList[2]
  float_dateTime = textList[1]
  date_value = xlrd.xldate_as_tuple(float_dateTime, workbook.datemode)
  date_value = datetime(*date_value[:5])
  if datetime.now() > date_value:
    continue
  date_value = date_value.strftime('%Y-%m-%d %H:%M:%S')
  textList[1] = date_value
  scheduler.add_job(SentChatRoomsMsg, 'date', run_date=date_value,kwargs={"name": name, "context": context})
  print("任务" + str(index) + ":\n待发送时间：" + date_value + "\n待发送到：" + name + "\n待发送内容：" + context + "\n******************************************************************************\n")
  index = index + 1
if index == 1:
  print("***没有任务需要执行***")
scheduler.start()