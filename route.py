from citygraph import *
from collections import deque

def main():
	cities_file = open('city-gps.txt','r')
	roads_file = open('road-segments.txt','r')
	g = Graph()
	process_files(cities_file, roads_file, g)
	test_sorting(g)

	initial_city = 'Milan,_Tennessee'
	goal_city = 'Ardmore,_Oklahoma'

	queue = deque
	queue.appendleft(())
	generic_search(g, 'bfs', )


def generic_search(g, search_type, queue, successor_param, goal):
	if search_type == 'bfs':
		pop = queue.pop
		push = queue.appendleft
	elif search_type == 'dfs':
		pop = queue.pop
		push = queue.append
	elif search_type == 'a*':
		pop = queue.get
		push = queue.put

	while(1):
		node = pop()
		if node[0] == goal: return node[3]
		if queue.empty(): return 'Failure'
		for s in g.successor(node[0], successor_param):
			s[3] += ',' + node[0]
			push(s)


	pass


def process_files(cities_file, roads_file, g):
	#Add all the cities to the graph
	for line in cities_file:
		temp = line.split(' ')
		if len(temp) < 3:
			g.insert_node(City(temp[0]))
		else:
			g.insert_node(City(temp[0], temp[1], temp[2]))
	unique_cities = g.nodes
	roads_discarded = 0
	roads_added = 0

	for line in roads_file:
		temp = line.split(' ')
		roads_added += 1
		if temp[0] in unique_cities and temp[1] in unique_cities:
			if temp[3] == '':
				temp[3] = '20'
			g.insert_edge(Road(temp[4]+":"+temp[0]+":"+temp[1], temp[0], temp[1], temp[2], temp[3]))
		elif 'JCT' in temp[0].upper() or 'JCT' in temp[1].upper():
			g.insert_node(City(temp[0]))
			unique_cities = g.nodes
		else:
			#print 'No city found for road: ' + line
			roads_discarded += 1
			roads_added -= 1

	print 'Number of roads: ' + str(roads_added)
	print 'Roads discarded: ' + str(roads_discarded)
	print 'Text files processed successfully'

	# test_city = 'Ardmore,_Oklahoma'
	# for road in g.edges:
	# 	conn = g.edges[road].connected_cities()
	# 	if test_city in conn:
	# 		print conn

	for edge in g.edges:
		road = g.edges[edge]
		conn = road.connected_cities()
		a = conn[0]
		b = conn[1]
		# if a == test_city or b == test_city:
		# 	print conn
		g.nodes[a].add_neighbor((b, road.time(), road.distance()))
		g.nodes[b].add_neighbor((a, road.time(), road.distance()))

	total_neighbors = 0
	num_cities = 0
	for node in g.nodes:
		city = g.nodes[node]
		total_neighbors += len(city.get_neighbors())
		num_cities += 1

	print 'Number of cities: ' + str(num_cities)
	print 'Average number of neighbors: ' + str(1.0*total_neighbors/num_cities)
	print 'City neighbors populated'

def test_sorting(g):
	test_city = 'Milan,_Tennessee'
	print 'Ordered by insertion'
	print g.nodes[test_city].get_neighbors()
	print 'Ordered by time'
	print g.successor(test_city, 'time')
	print 'Ordered by distance'
	print g.successor(test_city, 'distance')

if __name__ == '__main__':
	main()
