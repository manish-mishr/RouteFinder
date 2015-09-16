from operator import itemgetter

class City:

	def __init__(self, name, lat=0, lon=0):
		self.name = name
		self.lat = lat
		self.lon = lon
		self.neighbors = []

	def add_neighbor(self, neighbor):
		self.neighbors.insert(0,neighbor)

	def get_neighbors(self):
		return self.neighbors

class Road:

	def __init__(self, name, a, b, dist, speed):
		self.name = name
		self.a = a
		self.b = b
		self.dist = int(dist)
		self.speed = int(speed)

	def time(self):
		return  float(self.dist)/self.speed if self.speed != 0 else 10000000

	def distance(self):
		return self.dist

	def connected_cities(self):
		return (self.a, self.b)

	def equals(self, r):
		sconn = self.connected_cities()
		rconn = r.connected_cities()
		return sconn == rconn or sconn[::-1] == rconn

class Graph:
	nodes = {}
	edges = {}

	def __init__(self):
		pass

	def insert_node(self, n):
		self.nodes[n.name] = n

	def insert_edge(self, e):
		self.edges[e.name] = e

	def successor(self, city, ordering):
		n = self.nodes[city]
		neighbors = n.get_neighbors()
		if ordering == "time":
			sorted_neighbors = sorted(neighbors, key=itemgetter(1))
			return sorted_neighbors
		elif ordering == "distance":
			sorted_neighbors = sorted(neighbors, key=itemgetter(2))
			return sorted_neighbors
		else:
			 return neighbors
