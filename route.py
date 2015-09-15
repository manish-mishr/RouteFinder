

if __name__ == '__main__':
	main()

def main():
	cities_file = open('city-gps.txt','r')
	roads_file = open('road-segments.txt','r')
	g = Graph()
	#Add all the cities to the graph
	for line in cities_file:
		temp = line.split(' ')
		if temp.length() < 3:
			g.insert_node(City(temp[0]))
		else
			g.insert_node(City(temp[0], temp[1], temp[2]))

	for line in roads_file:
		temp = line.split(' ')
		g.insert_edge(Road(temp[4], temp[0], temp[1], temp[2], temp[3]))

	for edge in g.edges

class City:
	name = ""
	lat = 0
	lon = 0
	neighbors = []
	
	def __init__(self, name, lat=0, lon=0):
		self.name = name
		self.lat = lat
		self.lon = lon

	def successor(self, ordering):
		if ordering == "time":
			return neighbors
		else if ordering == "segments":
			return neighbors
		else if ordering == "distance":
			return neighbors

	def add_neighbor(self, neighbor):
		neighbors.add(neighbor)

class Road:
	name = ""
	a = ""
	b = ""
	length = 0
	speed = 0

	def __init__(self, name, a, b, length, speed):
		self.name = name
		self.a = a
		self.b = b
		self.length = length
		self.speed = speed

	def time(self):
		return 1.0*length/speed;

	def connected_cities(self):
		return (a, b)

class Graph:
	nodes = {}
	edges = {}

	def __init__(self):
		pass

	def insert_node(self, n):
		nodes[n.name] = n

	def insert_edge(self, e):
		edges[e.name] = e



