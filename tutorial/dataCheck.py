#!/usr/bin/env python
import json
import sqlite3

conn = sqlite3.connect('db.sqlite')
cursor = conn.execute("SELECT s.seccode,s.trustFee,s.manageFee,s.accumulatedUnitnv,s.unitnv,s.comeFrom,s1.trustFee,s1.manageFee,s1.accumulatedUnitnv,s1.unitnv,s1.comeFrom from product as s left join product as s1 on s.seccode = s1.seccode where s.comeFrom='1' and s1.comeFrom='2' order by s.seccode")

resultJson = []
for row in cursor:
    dict = {}
    flag = False
    for i in range(4):
        x = i + 1
        y = i + 5
        if y == 8 and y == 9:
            temp = ("0" + row[x]) if row[x].startswith('.') else row[x]
            if row[y] and (row[y].endswith('%') or row[y].endswith('--')):
                flag = True
                break
            if float(temp) != float(str(row[y])):
                flag = True
                break
        elif row[x] != row[y]:
                flag = True
    if flag:
        dict['fromProdma'] = {'seccode':row[0],'trustFee':row[1],'manageFee':row[2],'accumulatedUnitnv':row[3],'unitnv':row[4]}
        dict['fromEastmoney'] = {'seccode':row[0],'trustFee':row[6],'manageFee':row[7],'accumulatedUnitnv':row[8],'unitnv':row[9]}
        resultJson.append(dict)

print(json.dumps(resultJson))
