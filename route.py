from citygraph import *

def main():
	cities_file = open('city-gps.txt','r')
	roads_file = open('road-segments.txt','r')
	g = Graph()
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
			g.insert_edge(Road(temp[4], temp[0], temp[1], temp[2], temp[3]))
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

	test_city = 'Milan,_Tennessee'

	for road in g.edges:
		conn = g.edges[road].connected_cities()
		if test_city in conn:
			print conn
	break_at = 0
	for road in g.edges:
		conn = g.edges[road].connected_cities()
		a = conn[0]
		b = conn[1]
		break_at += 1
		if a == test_city or b == test_city:
			print conn
			print g.nodes[test_city].get_neighbors()
			break
		g.nodes[a].add_neighbor(b)
		g.nodes[b].add_neighbor(a)

	total_neighbors = 0
	num_cities = 0
	for node in g.nodes:
		city = g.nodes[node]
		if city.name == test_city:
			print city.get_neighbors() 
		total_neighbors += len(city.get_neighbors())
		num_cities += 1

	print 'Number of cities: ' + str(num_cities)
	print 'Average number of neighbors: ' + str(total_neighbors/num_cities)
	print 'City neighbors populated'

if __name__ == '__main__':
	main()





