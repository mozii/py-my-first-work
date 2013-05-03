#-*-coding:utf-8-*-
import urllib  
import urllib2  
import cookielib
import random
import sys
import json
import lxml
from pyquery import PyQuery as pq

type = sys.getfilesystemencoding()
#.decode('UTF-8').encode(type)

def start():
	print "####","\n",u"我们来玩一个游戏，只要你诚实，我就能读出你心里所想的某个人^_^。","\n",u"我会提问，请输入你的选择：1是yes，2是no，3是unknown，然后按下‘回车’。","\n","####","\n",u"准备好了吗？","\n"
	start = raw_input()
	while start != "1":
		print u"知道输入什么吧？"
		start = raw_input()
	print u"开始！","\n"

def index():
	cj = cookielib.CookieJar()  
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))  
	opener.addheaders = [('User-agent','Mozilla/5.0 (Windows NT 6.1; rv:19.0) Gecko/20100101 Firefox/19.0)')]  #头信息
	urllib2.install_opener(opener)  
	req = urllib2.Request("http://renlifang.msra.cn/Q20/index.aspx")  
	req.add_header("Referer","http://renlifang.msra.cn/Q20/index.aspx")  
	resp = urllib2.urlopen(req)  
	# print resp.read() 

def first():
	para = {
	    'a':"InitQuestionHandler",
		'sid':940037297,
		'uid':229719320
	    }
	req = urllib2.Request("http://renlifang.msra.cn/Q20/Handlers/HandlerQ20.ashx",urllib.urlencode(para))  
	req.add_header("Referer","http://renlifang.msra.cn/Q20/index.aspx")  
	resp = urllib2.urlopen(req)  
	result = resp.read()
	r = json.loads(result)
	print r["question"]
	writeData(r["question"])

def mind():
	para_yes = {
		'a':'GenerateQuestionHandler',
		'choice':"yes",
		'questfd':0,
		'sid':940037297,
		'uid':229719320
	}
	para_no = {
		'a':'GenerateQuestionHandler',
		'choice':"no",
		'questfd':0,
		'sid':940037297,
		'uid':229719320
	}
	para_unknow = {
		'a':'GenerateQuestionHandler',
		'choice':"unknow",
		'questfd':0,
		'sid':940037297,
		'uid':229719320
	}
	x = ["1","2","3"]
	mind = raw_input()
	while mind not in x:
		print "Try again"
		mind = raw_input()
	if mind == x[0]:
		mind = para_yes
	elif mind == x[1]:
		mind = para_no
	else:
		mind = para_unknow
	return mind

def answerQuestion(mind):
	req = urllib2.Request("http://renlifang.msra.cn/Q20/Handlers/HandlerQ20.ashx",urllib.urlencode(mind))  
	req.add_header("Referer","http://renlifang.msra.cn/Q20/index.aspx")  
	resp = urllib2.urlopen(req)
	result = resp.read()
	s = json.loads(result)
	if s["question"] == u"你所猜的人物是：":
		return s["question"]+s["entityresult"]
	else:
		return s["question"]

def justDo():

	first() 

	i = 0
	while i < 30:

		m = mind()
		choice = m["choice"]
		print choice,"\n"
		writeData(choice)

		answerQuestion(m)
		question = answerQuestion(m)

		if u"乱点的吧" in question or u"有没有在想" in question or u"你知道什么" in question:
			print u"哼。。。你乱点的，不跟你玩了"
			break
		elif u"你所猜的人物是：" in question:
			if "people.png" in question:
				question = question.replace("/App_Themes/cn/images/people.png","http://renlifang.msra.cn/App_Themes/cn/images/people.png").replace("/view.aspx","http://renlifang.msra.cn/view.aspx") 
			else:
				question = question.replace("/portrait.aspx","http://renlifang.msra.cn/portrait.aspx").replace("/view.aspx","http://renlifang.msra.cn/view.aspx")
			# question = question.replace("你所猜的人物是：","")
			writeData(question)
			d = pq(question)
			question = d('.entity-name-result').html()
			print u"你心里想的人物是：",question,"\n",u"可以打开YourSecret.html查看游戏记录和他的百科哦~~","\n",u"想玩的时候再来找我哦，我退出了，和人家说‘byebye’~","\n"
			bye = raw_input()
			y = ["byebye","Byebye","88","bye"]
			while bye not in y:
				print u"哼。。。"
				bye = raw_input()
			break
		else:
			print question
			writeData(question)
			i = i + 1


def writeData(data):
	file_object = open('YourSecret.html','a')
	data = data.encode('gb2312')
	file_object.write(data)
	file_object.write('<br>')
	file_object.close

start()
index()
justDo()