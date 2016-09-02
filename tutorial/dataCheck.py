#!/usr/bin/env python
import json

f = open('items.jl','rb')
f1 = open('tempList.txt','rb')
l = []
for line in f.readlines():
    l.append(json.loads(line.strip()))

l1 = json.load(f1)

sortedL1 = sorted(l1,key=lambda t: t['seccode'])
sortedL = sorted(l,key=lambda t: t['seccode'])

sortedL2 = []

i = 0
while i < len(sortedL):
    if sortedL[i]['seccode'] == sortedL[i+1]['seccode']:
	sortedL[i].update(sortedL[i+1])
	sortedL2.append(sortedL[i])	
	i += 2
    else:
	sortedL2.append(sortedL[i])
	i += 1


resultJson = []
n = 0
for index in range(len(sortedL1)):
    while n < len(sortedL2):
	if sortedL1[index]['seccode'] == sortedL2[n]['seccode']:
	    for key in sortedL2[n]:
		if key == "accumulatedUnitnv" or key == "unitnv":
		    temp = ("0" + sortedL1[index][key]) if sortedL1[index][key].startswith('.') else sortedL1[index][key]
		    if sortedL2[n][key].endswith('%') or sortedL2[n][key].endswith('--'):
			dict = {}
			dict['fromProdma'] = sortedL1[index]
			dict['fromEastmoney'] = sortedL2[n]
			resultJson.append(dict)
#			print("^^^^^^^^^^^^^^^^^^^^")
#			print sortedL1[index]
#			print sortedL2[n]
#			print("^^^^^^^^^^^^^^^^^^^^^")
			break
		    if float(temp) != float(str(sortedL2[n][key])):
			dict = {}
			dict['fromProdma'] = sortedL1[index]
			dict['fromEastmoney'] = sortedL2[n]
			resultJson.append(dict)
#			print("#####################")
#		    	print sortedL1[index]
#			print sortedL2[n]
#			print("#####################")
		    	break
		elif sortedL1[index][key] != sortedL2[n][key]:
		    dict = {}
		    dict['fromProdma'] = sortedL1[index]
	            dict['fromEastmoney'] = sortedL2[n]
		    resultJson.append(dict)
#	            print("#####################")
#		    print sortedL1[index]
#		    print sortedL2[n]
#	            print("#####################")
		    break
#		print('-----------------')
#		print sortedL1[index][key]
#               print sortedL2[n][key]
#		print('-----------------')
	    n += 1
        elif sortedL1[index]['seccode'] < sortedL2[n]['seccode']:
	   # print( sortedL1[index]['seccode'] + "..." + sortedL[n]['seccode'])
            break 
        elif sortedL1[index]['seccode'] > sortedL2[n]['seccode']:
            n += 1
print(json.dumps(resultJson))
