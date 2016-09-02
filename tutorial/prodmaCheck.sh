#!/bin/sh

temp1='tempSeccodeList.txt'
temp2='items.jl'

test -f $temp1 && rm -rf $temp1
test -f "$temp2" && rm -rf "$temp2"

scrapy crawl prodma >/dev/null 2>&1 

if [ $? -eq 0 ] && [ -f "$temp1" ];then
 echo 'now crawl data from fund.eastmoney.com' 
 cat $temp1 | xargs -I {} scrapy crawl eastmoney -a productId={}
else
 echo 'get Seccode from Server Failed!'
 exit 1
fi

if [ $? -eq 0 ];then
 ./dataCheck.py > mylog.txt
 echo 'Success!Congratulation' 
 exit 0
else
 echo 'get Data from fund.eastmoney.com failed!'
 exit 1
fi
