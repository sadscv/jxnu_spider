import requests
import re
from PIL import Image
from io import BytesIO
import json
from learn import *

params={
	"__EVENTTARGET":"",
	"__EVENTARGUMENT":"",
	"__LASTFOCUS":"",
	"__VIEWSTATE":"",
	"__EVENTVALIDATION":"",
	"_ctl0:cphContent:ddlUserType":"Student",
	"_ctl0:cphContent:txtUserNum":"",
	"_ctl0:cphContent:txtPassword":"",
	"_ctl0:cphContent:txtCheckCode":"",
	"_ctl0:cphContent:btnLogin":"登录"
}
header={
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.9',
	'Connection':'keep-alive',
	'Host':'jwc.jxnu.edu.cn',
	'Referer':'http://jwc.jxnu.edu.cn/Portal/Index.aspx',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400'
}

s=requests.session()
login_page="http://jwc.jxnu.edu.cn/Portal/LoginAccount.aspx?t=account"
xuehao_list=[]

def get_token(page):
	token_html=requests.get(page,headers=header).text
	# print(token_html)
	code_url=re.search('imgPasscode\" src=\"(.*?)\" border=\"0\" style=\"',token_html).group(1)
	params["__VIEWSTATE"]=re.search('id=\"__VIEWSTATE\" value=\"(.*?)\"',token_html).group(1)
	params["__EVENTVALIDATION"]=re.search('id=\"__EVENTVALIDATION\" value=\"(.*?)\"',token_html).group(1)
	image = Image.open(BytesIO(requests.get("http://jwc.jxnu.edu.cn/Portal/"+code_url).content))
	# image.show()
	return get_code(image)
def login(username,password):
	params["_ctl0:cphContent:txtUserNum"]=username
	params["_ctl0:cphContent:txtPassword"]=password
	params["_ctl0:cphContent:txtCheckCode"]=get_token(login_page)
	print("code:"+params["_ctl0:cphContent:txtCheckCode"])
	res=s.post(login_page,data=params,headers=header)
	if "验证码错误" in res.text:
		print("验证码错误,正在重试")
		return login(username,password)
	else:
		print("登录成功!")

def get_personal_kebiao():
	personal_kebiao_params={
	"__EVENTTARGET":"",
	"__EVENTARGUMENT":"",
	"__VIEWSTATE":"",
	"__EVENTVALIDATION":"",
	"_ctl1:ddlSterm":"2018/9/1 0:00:00",
	"_ctl1:btnSearch":"确定"
	}
	kebiao_url="http://jwc.jxnu.edu.cn/User/default.aspx?&&code=111&uctl=MyControl%5cxfz_kcb.ascx&MyAction=Personal"
	kebiao_header=header
	kebiao_header["Referer"]="http://jwc.jxnu.edu.cn/User/default.aspx?&&code=111&uctl=MyControl%5cxfz_kcb.ascx&MyAction=Personal"
	kebiao_token_html=s.post(kebiao_url,headers=kebiao_header).text
	personal_kebiao_params["__VIEWSTATE"]=re.search('id=\"__VIEWSTATE\" value=\"(.*?)\"',kebiao_token_html).group(1)
	personal_kebiao_params["__EVENTVALIDATION"]=re.search('id=\"__EVENTVALIDATION\" value=\"(.*?)\"',kebiao_token_html).group(1)
	res=s.post(kebiao_url,data=personal_kebiao_params,headers=kebiao_header)
	kebiao_html=res.text
	kebiao_html=kebiao_html.lower()
	table=re.search('<div id=\"_ctl1_newkcb\">.*?<table.*?>(.*?)</table>.*?</div>',kebiao_html,re.S).group(1)
	table=str_fix(table)
	trs=re.findall('<tr>(.*?)</tr>',table,re.S)
	del trs[0]
	del trs[len(trs)-1]
	for tr in trs:
		td=re.findall('<td.*?>(.*?)</td>',tr,re.S)
		if not td[0].isdigit():
			del td[0]
		print(td)

def get_other_kebiao(xuehao):
	tds=[]
	kebiao_params={
		"__VIEWSTATE":"",
		"__EVENTVALIDATION":"",
		"_ctl11:ddlSterm":"2018/9/1 0:00:00",
		"_ctl11:btnSearch":"确定"
	}
	kebiao_by_username_url="http://jwc.jxnu.edu.cn/MyControl/All_Display.aspx?UserControl=Xfz_Kcb.ascx&UserType=Student&UserNum={userid}"
	kebiao_url=kebiao_by_username_url.format(userid=xuehao)
	kebiao_header=header
	kebiao_header["Referer"]="http://jwc.jxnu.edu.cn/User/default.aspx?&&code=119&uctl=MyControl%5call_searchstudent.ascx"
	kebiao_token_html=s.post(kebiao_url,headers=kebiao_header).text
	kebiao_params["__VIEWSTATE"]=re.search('id=\"__VIEWSTATE\" value=\"(.*?)\"',kebiao_token_html).group(1)
	kebiao_params["__EVENTVALIDATION"]=re.search('id=\"__EVENTVALIDATION\" value=\"(.*?)\"',kebiao_token_html).group(1)
	res=s.post(kebiao_url,data=kebiao_params,headers=kebiao_header)
	kebiao_html=res.text
	kebiao_html=kebiao_html.lower()
	table=re.search('<table.*?>(.*?)</table>',kebiao_html,re.S).group(1)
	table=str_fix(table)
	trs=re.findall('<tr>(.*?)</tr>',table,re.S)
	del trs[0]
	del trs[0]
	del trs[len(trs)-1]
	for tr in trs:
		td=re.findall('<td.*?>(.*?)</td>',tr,re.S)
		if not td[0].isdigit():
			del td[0]
		print(td)
		tds.append(td)
	return json.dumps(tds)

def get_kebiao_by_name(name):
	search_people(name)
	kebiao_by_username_url="http://jwc.jxnu.edu.cn/MyControl/All_Display.aspx?UserControl=Xfz_Kcb.ascx&UserType=Student&UserNum={userid}"
	kebiao_url=kebiao_by_username_url.format(userid=xuehao_list[0])
	kebiao_header=header
	kebiao_header["Referer"]="http://jwc.jxnu.edu.cn/User/default.aspx?&&code=119&uctl=MyControl%5call_searchstudent.ascx"
	kebiao_token_html=s.post(kebiao_url,headers=kebiao_header).text
	kebiao_params=params
	kebiao_params["__VIEWSTATE"]=re.search('id=\"__VIEWSTATE\" value=\"(.*?)\"',kebiao_token_html).group(1)
	kebiao_params["__EVENTVALIDATION"]=re.search('id=\"__EVENTVALIDATION\" value=\"(.*?)\"',kebiao_token_html).group(1)
	kebiao_params["_ctl11:ddlSterm"]="2018/9/1 0:00:00"
	kebiao_params["_ctl11:btnSearch"]="确定"
	res=s.post(kebiao_url,data=kebiao_params,headers=kebiao_header)
	kebiao_html=res.text
	kebiao_html=kebiao_html.lower()
	table=re.search('<table.*?>(.*?)</table>',kebiao_html,re.S).group(1)
	table=str_fix(table)
	trs=re.findall('<tr>(.*?)</tr>',table,re.S)
	# del trs[0]
	# del trs[0]
	# del trs[len(trs)-1]
	for tr in trs:
		td=re.findall('<td.*?>(.*?)</td>',tr,re.S)
		# if not td[0].isdigit():
		# 	del td[0]
		print(td)

def search_people(name):
	tds=[]
	search_url="http://jwc.jxnu.edu.cn/User/default.aspx?&&code=119&uctl=MyControl%5call_searchstudent.ascx"
	search_params={
	    "__EVENTTARGET":"",
	    "__EVENTARGUMENT":"",
	    "__LASTFOCUS":"",
	    "__VIEWSTATE":"",
	    "__EVENTVALIDATION":"",
	    "_ctl1:rbtType":"SQL",
	    "_ctl1:txtKeyWord":name,
	    "_ctl1:ddlType":"姓名",
	    "_ctl1:ddlSQLType":"精确",
	    "_ctl1:btnSearch":"查询"
	}
	search_header=header
	search_header["Referer"]="http://jwc.jxnu.edu.cn/User/default.aspx?&code=119&&uctl=MyControl\\all_searchstudent.ascx"
	search_token_html=s.post(search_url,headers=search_header).text
	search_params["__VIEWSTATE"]=re.search('id=\"__VIEWSTATE\" value=\"(.*?)\"',search_token_html).group(1)
	search_params["__EVENTVALIDATION"]=re.search('id=\"__EVENTVALIDATION\" value=\"(.*?)\"',search_token_html).group(1)
	res=s.post(search_url,data=search_params,headers=search_header)
	result_html=res.text
	table=re.search('<table id=\"_ctl1_rbtType\" border=\"0\" style=\"height:8px;width:184px;\">(.*)</table>',result_html,re.S).group(1)
	table=str_fix(table)
	trs=re.findall('<tr.*?>(.*?)</tr>',table,re.S)
	del trs[0]
	del trs[0]
	del trs[len(trs)-1]
	for tr in trs:
		td=re.findall('<td.*?>(.*?)</td>',tr,re.S)
		for j in td:
			if j.isdigit():
				xuehao_list.append(j)
		print(td)
		tds.append(td)
	return json.dumps(tds)
def str_fix(str):
	str=str.replace("\r","")
	str=str.replace("\n","")
	str=str.replace("\t","")
	str=str.replace("<br>","")
	str=str.replace("&nbsp;","")
	str=str.replace(" ","")
	str=re.sub(re.compile(r'(?!(<td.*?>)|(</td>)|(<tr.*?>)|(</tr>))<.*?>',re.S), '', str)
	return str

def get_photo(xuehao):
	print(xuehao)
	photo_url="http://jwc.jxnu.edu.cn/StudentPhoto/{id}.jpg".format(id=xuehao)
	photo_header={
		"Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "zh-CN,zh;q=0.9",
		"Connection": "keep-alive",
		"Host": "jwc.jxnu.edu.cn",
		"Referer": "http://jwc.jxnu.edu.cn/Portal/Index.aspx",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
	}
	res=s.get(photo_url,headers=photo_header)
	im=Image.open(BytesIO(res.content))
	im.show()

def get_report_card():
	guake_list=[]
	report_url="http://jwc.jxnu.edu.cn/MyControl/All_Display.aspx?UserControl=xfz_cj.ascx&Action=Personal"
	report_header={
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "zh-CN,zh;q=0.9",
		"Cache-Control": "max-age=0",
		"Connection": "keep-alive",
		"Referer": "http://jwc.jxnu.edu.cn/User/Default.aspx",
		"Upgrade-Insecure-Requests": "1",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
	}
	res=s.get(report_url,headers=report_header)
	table=re.search('<table.*?>(.*?)</table>',res.text,re.S).group(1)
	table=str_fix(table)
	trs=re.findall('<tr.*?>(.*?)</tr>',table,re.S)
	for tr in trs:
		td=re.findall('<td.*?>(.*?)</td>',tr,re.S)
		if not td[0].isdigit():
			del td[0]
		if len(td)==7:
			if td[3].isdigit():
				if int(td[3])<60 and int(td[4])<60:
					guake_list.append(td)
		print(td)
	print("挂科数:"+str(len(guake_list)))
	print(guake_list)
if __name__ == '__main__':
	login("201626203044","362421199712231412")
	# get_personal_kebiao()
	# # # for i in xuehao_list:
	# # # 	get_photo(i)
	# # get_report_card()
	# search_people("李丹")
	get_photo(201526202045)
	# print(get_other_kebiao(201625101103))