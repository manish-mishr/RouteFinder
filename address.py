
import itertools

def main():
	mylist=[ [ 'Amplifier','Banister','Candel','Doorknob','Elephant'], ['Frank','George','Heather','Irene','Jerry',], ['Kirkwood','Lake','Maxwell','North','Orange'] ]

	oldlist = list(itertools.product(*mylist))

	process_list=[item for item in oldlist if not((item[0]=='Doorknob' and  item[1]=='Frank') or (item[1]=='George' and item[2]=='Kirkwood')or(item[1]=='Heather' and item[2]=='Orange') or (item[0]=='Banister' and item[1]=='Irene') or (item[0]=='Elephant' and item[2]=='North')
	or(item[0]=='Amplifier' and item[2]=='Maxwell'))]

	list_amplifier=[item for item in process_list if item[0]=='Amplifier']
	list_banister=[item for item in process_list if item[0]=='Banister']
	list_candel=[item for item in process_list if item[0]=='Candel']
	list_doorknob=[item for item in process_list if item[0]=='Doorknob']
	list_Elephant=[item for item in process_list if item[0]=='Elephant']

	for la in list_amplifier:
		for lb in list_banister:
			for lc in list_candel:
				for ld in list_doorknob:
					for le in list_Elephant:
						if test_combination(la, lb, lc, ld, le):
							if test_constraints(la, lb, lc, ld, le):
								print str(la) + '\n' + str(lb) + '\n' + str(lc) + '\n' + str(ld) + '\n' + str(le)



def test_combination(set1, set2, set3, set4, set5):
	if set1[1] == set2[1]  or set1[1] == set3[1] or set1[1] == set4[1] or set1[1] == set5[1]:
		return False
	if set1[2] == set2[2]  or set1[2] == set3[2] or set1[2] == set4[2] or set1[2] == set5[2]:
		return False

	if set2[1] == set3[1] or set2[1] == set4[1] or set2[1] == set5[1]:
		return False
	if set2[2] == set3[2] or set2[2] == set4[2] or set2[2] == set5[2]:
		return False

	if set3[1] == set4[1] or set3[1] == set5[1]:
		return False
	if set3[2] == set4[2] or set3[2] == set5[2]:
		return False

	if set4[1] == set5[1] or set4[2] == set5[2]:
		return False

	return True

class Neighborhood:

	def __init__(self):
		self.houses = []

	def add_house(self, h):
		self.houses.append(h)

	def getHouse_Name(self, name):
		for h in self.houses:
			if h.name == name:
				return h
		return 'Failure'

	def getHouse_Item(self, item):
		for h in self.houses:
			if h.item == item:
				return h
		return 'Failure'

	def getHouse_Street(self, street):
		for h in self.houses:
			if h.street == street:
				return h
		return 'Failure'

	def __str__(self):
		out = ''
		for h in self.houses:
			out += str(h)
		return out

	def __repr__(self):
		self.__str__()

class House:

	def __init__(self, name, item, street):
		self.name = name
		self.item = item
		self.street = street

	def __str__(self):
		return '('+self.item+',' + self.name + ',' + self.street + ')'

	def __repr__(self):
		return self.__str__()


def test_constraints(set1, set2, set3, set4, set5):

	n = Neighborhood()
	n.add_house(House(set1[1],set1[0],set1[2]))
	n.add_house(House(set2[1],set2[0],set2[2]))
	n.add_house(House(set3[1],set3[0],set3[2]))
	n.add_house(House(set4[1],set4[0],set4[2]))
	n.add_house(House(set5[1],set5[0],set5[2]))

	house_list =  ['Kirkwood','Lake','Maxwell','North','Orange']

	d = {}
	d['Banister'] = n.getHouse_Item('Candel')

	irene_item = n.getHouse_Name('Irene').item
	d[irene_item] = n.getHouse_Item('Banister')

	if 'Doorknob' in d.keys():
	 	return False
	d['Doorknob'] = n.getHouse_Name('Frank')

	if 'Amplifier' in d.keys():
		return False
	d['Amplifier'] = n.getHouse_Street('Maxwell')

	if 'Elephant' in d.keys():
		return False
	d['Elephant'] = n.getHouse_Street('North')

	if d[n.getHouse_Street('Lake').item] != n.getHouse_Street('Kirkwood'):
		return False

	if d[n.getHouse_Street('Kirkwood').item] != n.getHouse_Name('George'):
		return False

	if d[n.getHouse_Street('Orange').item] != n.getHouse_Name('Heather'):
		return False

	if d[n.getHouse_Name('Heather').item] != n.getHouse_Name('Jerry'):
		return False

	if d[n.getHouse_Street('Maxwell').item] != n.getHouse_Item('Elephant'):
		return False

	solution = set()
	for k in d.keys():
		solution.add(d[k])
	if len(solution) == 5:
		return True

	return False




if __name__ == '__main__':
	main()
