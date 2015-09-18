from citygraph import *
from collections import deque
from Queue import PriorityQueue
import sys

def main():
	cities_file = open('city-gps.txt','r')
	roads_file = open('road-segments.txt','r')
	g = Graph()
	process_files(cities_file, roads_file, g)
	#test_sorting(g)

	argv = sys.argv
	initial_city = argv[1]
	goal_city = argv[2]
	optimize = argv[3]
	search_algo = argv[4]

	if not (initial_city in g.nodes) or not (goal_city in g.nodes):
		print 'Invalid input'
		return

	print(g.heuristic(initial_city, goal_city))

	if search_algo == 'bfs' or search_algo == 'dfs':
		queue = deque()
		queue.appendleft((initial_city, 0, 0, ''))
	elif search_algo == 'astar':
		queue = PriorityQueue()
		queue.put((g.heuristic(initial_city, goal_city),(initial_city, 0, 0, '')))
	else:
		print 'Invalid input'
		return

	ans = generic_search(g, search_algo, queue, optimize, goal_city)
	print ans
	answer_string = str(ans[2]) + ' ' + str(ans[1])
	c = g.nodes[ans[0]]
	route_str = ''
	while c.parent != '' and c.name != initial_city:
		route_str = c.name + ' ' + route_str
		c = g.nodes[c.parent.name]
	route_str = initial_city + ' ' + route_str[:-1]
	print answer_string + ' ' + route_str


def generic_search(g, search_type, queue, successor_param, goal):
	if search_type == 'bfs':
		pop = queue.pop
		push = queue.appendleft
	elif search_type == 'dfs':
		pop = queue.pop
		push = queue.append
	elif search_type == 'astar':
		pop = queue.get
		push = queue.put
	else:
		return 'Invalid search type'

	seen = {}

	while(1):
		if search_type != 'astar' and len(queue) == 0:
			return 'Failure'
		elif search_type == 'astar' and queue.empty():
			return 'Failure'
		node = pop()
		if search_type == 'astar':
			#print node
			node = node[1]
		if node[0] == goal: return node
		seen[node[0]] = node[0]
		for s in g.successor(node[0], successor_param):
			if s[0] in seen:
				continue
			s_prime = (s[0], s[1]+node[1], s[2]+node[2])
			child_city = g.nodes[s[0]]
			parent_city = g.nodes[node[0]]
			parent_city.add_child(child_city)
			child_city.set_parent(parent_city)
			if search_type == 'astar':
				s_prio = (g.heuristic(s[0], goal), s_prime)
				push(s_prio)
			else:
				push(s_prime)


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
		if 'JCT' in temp[0].upper() or 'JCT' in temp[1].upper():
			if 'JCT' in temp[0].upper() and not temp[0] in unique_cities:
				g.insert_node(City(temp[0]))
			if 'JCT' in temp[1].upper() and not temp[1] in unique_cities:
				g.insert_node(City(temp[1]))
			unique_cities = g.nodes
		if temp[0] in unique_cities and temp[1] in unique_cities:
			if temp[3] == '':
				temp[3] = '20'
			g.insert_edge(Road(temp[4]+":"+temp[0]+":"+temp[1], temp[0], temp[1], temp[2], temp[3]))
		else:
			#print 'No city found for road: ' + line
			roads_discarded += 1
			roads_added -= 1

	print 'Number of roads: ' + str(roads_added)
	print 'Roads discarded: ' + str(roads_discarded)
	print 'Text files processed successfully'

	# test_city = 'Jct_I-465_&_IN_37_S,_Indiana'
	# for road in g.edges:
	# 	conn = g.edges[road].connected_cities()
	# 	if test_city in conn:
	# 		print conn

	for edge in g.edges:
		road = g.edges[edge]
		conn = road.connected_cities()
		a = conn[0]
		b = conn[1]
		g.nodes[a].add_neighbor((b, road.time(), road.distance(), ''))
		g.nodes[b].add_neighbor((a, road.time(), road.distance(), ''))

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
	test_city = 'Jct_I-465_&_IN_37_S,_Indiana'
	print 'Ordered by insertion'
	print g.nodes[test_city].get_neighbors()
	print 'Ordered by time'
	print g.successor(test_city, 'time')
	print 'Ordered by distance'
	print g.successor(test_city, 'distance')

if __name__ == '__main__':
	main()
