from operator import itemgetter
from math import sin, cos, sqrt, atan2, radians

class City:

	def __init__(self, name, lat=0, lon=0):
		self.name = name
		self.lat = float(lat)
		self.lon = float(lon)
		self.neighbors = []
		self.children = []
		self.parent = ''

	def add_neighbor(self, neighbor):
		self.neighbors.insert(0,neighbor)

	def get_neighbors(self):
		return self.neighbors

	def add_child(self, child):
		self.children.insert(0,child)

	def set_parent(self, p):
		if self.parent != '':
			return
		else:
			self.parent = p

class Road:

	def __init__(self, name, a, b, dist, speed):
		self.name = name
		self.a = a
		self.b = b
		self.dist = int(dist)
		self.speed = int(speed)

	def time(self):
		if self.speed == 0:
			self.speed = 20
		return  float(self.dist)/self.speed

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

	def successor(self, c):
		if type(c) == tuple:
			city = c[0]
		else:
			city = c
		n = self.nodes[city]
		return n.get_neighbors()

	#Using the crows-flight distance, which is well documented online but this
	#code is taken from http://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude-python
	#with slight modifications (miles vs. km)
	def heuristic(self, cn1, cn2, param, data):
		c1 = self.nodes[cn1]
		c2 = self.nodes[cn2]
		if c1.lat == 0 or c1.lon == 0 or c2.lat == 0 or c2.lon == 0:
			return 0
		# approximate radius of earth in miles
		R = 3960.0

		lat1 = radians(c1.lat)
		lon1 = radians(c1.lon)
		lat2 = radians(c2.lat)
		lon2 = radians(c2.lon)

		dlon = lon2 - lon1
		dlat = lat2 - lat1

		a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
		c = 2 * atan2(sqrt(a), sqrt(1 - a))

		distance = R * c

		if param == 'distance':
			if distance == 0:
				return distance
			return 1.0/distance
		elif param == 'time':
			if data == 0:
				data = 20
			return float(distance)/data
		elif param == 'segments':
			if cn1 == cn2:
				return 0
			return float(data)/distance
