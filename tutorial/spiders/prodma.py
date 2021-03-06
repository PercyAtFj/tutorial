# -*- coding: utf-8 -*-
import scrapy
import base64
import re
import sys
import os
import json
import sqlite3
import datetime
sys.path.append(os.path.abspath(''))
import digestAuthentication
import rsaUtil
from scrapy.http import Request, FormRequest
from scrapy.utils.project import get_project_settings


class ProdmaSpider(scrapy.Spider):
    name = 'prodma'
    settings = get_project_settings()
    url = settings['PRODMA_DOMAIN']
    start_urls = ['http://' + url + '/prodma/product/productDataCheck/list/']
    db = settings['PRODMA_DATABASE']
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        #"Host": "eworksh.xyzq.com.cn",
        #"Origin": "https://eworksh.xyzq.com.cn",
        "Pragma":"no-cache",
        #"Referer":"https":"//eworksh.xyzq.com.cn/prodma/login",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    def create_table(self, filename):
        conn = sqlite3.connect(filename)
        conn.execute("""create table if not exists product
                     (seccode text not null,
                      trustFee text,
                      manageFee text,
                      accumulatedUnitnv text,
                      unitnv text,
                      comeFrom int not null,
                      updateDate text,
                      primary key(seccode,comeFrom)
                      )""")
        conn.commit()
        return conn

    def parse_item(self,response):
	conn = self.create_table(self.db)
        d = json.loads(response.body)
        l = d['data']

        for item in l:
	    conn.execute('replace into product values(?,?,?,?,?,?,?)',
                          (item.get("seccode"), item.get("trustFee"), item.get("manageFee"), item.get("accumulatedUnitnv"), item.get("unitnv"), "1", datetime.datetime.now().date()))
	
	seccodes = []
        for line in l:
            seccodes.append(line['seccode'])
        seccodeStr = ','.join(seccodes)
        f = open('tempSeccodeList.txt','wb')
        f.write(seccodeStr)
        f.close()

	if conn is not None:
            conn.commit()
            conn.close()

        #os.system('cd /home/vagrant/lixc/tutorial/tutorial && scrapy crawl eastmoney -a productId=%s' % seccodeStr)

    def after_login(self, response) :
	return [Request('http://' + self.url + '/prodma/product/productDataCheck/list/', meta = {'cookiejar' : 1}, callback = self.parse_item)]

    def start_requests(self):
        return [Request("http://" + self.url + "/prodma/login", meta = {'cookiejar' : 1}, callback = self.post_login)]

    def get_rsaPublicKey(self,response):
	publicKeyExponent = re.search( r'publicKeyExponent = "(.*?)";',response.body,re.M) 
	publicKeyModulus = re.search( r'publicKeyModulus = "(.*?)";',response.body,re.M)	
	print(publicKeyExponent.group(1))
	print(publicKeyModulus.group(1))
	return [publicKeyExponent.group(1),publicKeyModulus.group(1)]
	
    def post_login(self, response):
        print 'Preparing login'
	username = self.settings["PRODMA_USERNAME"]
	password = self.settings["PRODMA_PASSWORD"]
	publicKeyPremeters = self.get_rsaPublicKey(response)			
		
	headers = response.headers['WWW-Authenticate']
	digestau = digestAuthentication.get_DigestAuthentication()
	da = digestau.authentication
	md5 = digestau.md5
	header = digestau.head
	
	da.registerCredentials(username,md5(password))
	header.setCredantials(username,md5(password))
	header.parse(headers)
        a = header.generate("login","post")
	a = a.replace("'", "\"");
	password = base64.b64encode(password)
	publicKey = rsaUtil.get_RSAUtil().getKeyPair(publicKeyPremeters[0], "",publicKeyPremeters[1])
	password = rsaUtil.get_RSAUtil().encryptedString(publicKey, password)
	
	jsessionid = response.headers['Set-Cookie'].split(';')[0]
	self.headers['Authorization'] = a
        return [FormRequest('http://' + self.url + '/prodma/login/setcookie_post', 
                    meta = {'cookiejar' : response.meta['cookiejar']},
                    headers = self.headers,  #注意此处的headers
		    formdata = {
                    	'username': username,
                    	'password': password
                    },
                    callback = self.after_login,
                    dont_filter = True
                )]
