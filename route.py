'''
Thijs Benschop
Manish Kumar
B551 - A1
Programming problem #2

Which search is best for which routing option?:
	Intuitively, BFS will give the best routing for the 'segments' routing option. This is because it will consider all paths with n turns before considering those with n+1 turns. In this way
	we can guarantee that the fewest segments are generated. For the other two routing options, A* gives the best results as BFS/DFS have no knowledge of these options, and A* is optimized
	to find the appropriate paths.
Which algorithm is fastest?
	A* is fastest by far; On SOIC linux machines, A* can compute the route from Bloomington, Indiana to Fort Kent, Maine in about 30 seconds, while BFS takes about 2 minutes and 30 seconds.
	DFS takes too long with this far of a path, and I had to terminate the search early. A*'s notion of prirtiy really helps to focus the search instead of considering unncessary paths in directions
	which may not be desirable.
Which heuristic was used?
	There were 3 different heuristics used:
	Distance: We used the computation of "crow's flight" distance from the latitude and longitude of the current city to the goal. Then, to make the city that is closest have the highest priority,
	we took the inverse of this number (i.e. 1/distance), to that shorter distances have larger priorities.
	Time: For this, we also used the crow's flight distance, but incorporated the speed limit of the next road. We took distance/speed, giving the time required to travel to in a straight line to the
	goal on that road.
	Segments: For this optimization, we used the heuristic which took into account the length of the road. We wanted to take longer roads, which would get closed to the destination. The
	calculation for this is length/distance, where distance is again crows flight distance. This gives the higher priority to long roads coming from the same node, which will theoretically get closer
	to the goal node.

	We feel these heuristics work fairly well, but there are some bugs. For one, not every road had a corresponding speed limit. For these roads, we gave a set value of 20mph. This leads to some
	non-optimal solutions, considering the time calculation could be thrown off by this assumed speed limit. Additionally, all of the heuristics used gave numbers < 1, so the number of moves taken so
	far had a more significant impact on the priority than the heuristic.

'''

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



	if search_algo == 'bfs' or search_algo == 'dfs':
		queue = deque()
		queue.appendleft((initial_city, 0, 0, ''))
	elif search_algo == 'astar':
		queue = PriorityQueue()
		queue.put((g.heuristic(initial_city, goal_city, 'distance', 0), (initial_city, 0, 0, 0)))
	else:
		print 'Invalid input'
		return

	ans = generic_search(g, search_algo, queue, optimize, goal_city)
	if ans == 'Failure':
		print ans
		return

	c = g.nodes[ans[0]]
	route_str = ''
	dist_traveled = 0
	time_traveled = 0
	last_city = c.name
	route_str = c.name + ' ' + route_str
	c = g.nodes[c.parent.name]
	while c.parent != '' and c.name != initial_city:
		for e in g.edges:
			if last_city in e and c.name in e:
				dist_traveled += g.edges[e].distance()
				time_traveled += g.edges[e].time()
		last_city = c.name
		route_str = c.name + ' ' + route_str
		c = g.nodes[c.parent.name]

	for e in g.edges:
		if last_city in e and initial_city in e:
			dist_traveled += g.edges[e].distance()
			time_traveled += g.edges[e].time()

	route_str = initial_city + ' ' + route_str[:-1]
	print str(dist_traveled) + ' ' + str(time_traveled) + ' ' + route_str


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
		for s in g.successor(node[0]):
			if s[0] in seen:
				continue
			s_prime = (s[0], node[1]+1, s[2], s[3])
			child_city = g.nodes[s[0]]
			parent_city = g.nodes[node[0]]
			parent_city.add_child(child_city)
			child_city.set_parent(parent_city)
			if search_type == 'astar':
				s_prio = (g.heuristic(s[0], goal, successor_param, s_prime[3] if successor_param == 'time' else s_prime[2]) + s_prime[1], s_prime)
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

	for edge in g.edges:
		road = g.edges[edge]
		conn = road.connected_cities()
		a = conn[0]
		b = conn[1]
		g.nodes[a].add_neighbor((b, 0, road.distance(), road.speed))
		g.nodes[b].add_neighbor((a, 0, road.distance(), road.speed))

	total_neighbors = 0
	num_cities = 0
	for node in g.nodes:
		city = g.nodes[node]
		total_neighbors += len(city.get_neighbors())
		num_cities += 1

	print 'Number of cities: ' + str(num_cities)
	print 'Average number of neighbors: ' + str(1.0*total_neighbors/num_cities)
	print 'City neighbors populated'


if __name__ == '__main__':
	main()
