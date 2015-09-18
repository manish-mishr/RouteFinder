#!/usr/bin/env python
import itertools
mylist=[ [ 'Amplifier','Banister','Candel','Doorknob','Elephant'], ['Frank','George','Heather','Irene','Jerry',],  		   		['Kirkwood','Lake','Maxwell','North','Orange'] ]

oldlist = list(itertools.product(*mylist))
print len(oldlist)

process_list=[item for item in oldlist if not((item[0]=='Doorknob' and  item[1]=='Frank') or (item[1]=='George' and item[2]=='Kirkwood')or(item[1]=='Heather' and item[2]=='Orange') or (item[0]=='Banister' and item[1]=='Irene') or (item[0]=='Elephant' and item[2]=='North')
or(item[0]=='Amplifier' and item[2]=='Maxwell'))]

print len(process_list)

list_amplifier=[item for item in process_list if item[0]=='Amplifier']
list_banister=[item for item in process_list if item[0]=='Banister']
list_candel=[item for item in process_list if item[0]=='Candel']
list_doorknob=[item for item in process_list if item[0]=='Doorknob']
list_elephant=[item for item in process_list if item[0]=='Elephant']

#print list_banister

test_list=[]
for item_candel in list_candel:
	unique_set=set()
	unique_set.add(item_candel[1])
	unique_set.add(item_candel[2])
	test_list.append(item_candel)
	for item_banister in list_banister:
		if item_candel[1] in unique_set or item_candel[2] in unique_set: 
			pass
		else:
			unique_set.add(item_banister[1])
			unique_set.add(item_banister[2])
			test_list.append(item_banister)
			for item_amplifier in list_amplifier:
				if item_amplifier[1] in unique_set or item_amplifier[2] in unique_set: 
					pass
				else:
					unique_set.add(item_amplifier[1])
					unique_set.add(item_amplifier[2])
					test_list.append(item_amplifier)
					for item_doorknob in list_doorknob:
						if item_doorknob[1] in unique_set or item_doorknob[2] in unique_set: 
							pass
						else:
							unique_set.add(item_doorknob[1])
							unique_set.add(item_doorknob[2])
							test_list.append(item_doorknob)
							for item_elephant in list_elephant:
								if item_elephant[1] in unique_set or item_elephant[2] in unique_set: 
									pass
								else:
									unique_set.add(item_elephant[1])
									unique_set.add(item_elephant[2])
									test_list.append(item_elephant)
									print unique_set
									name=raw_input("y")
#print test_list










