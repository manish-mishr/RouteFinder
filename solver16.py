#!/usr/bin/env python

import math
import copy
from Queue import PriorityQueue
from sys import argv

script, filename = argv

frontier=PriorityQueue()

matrix=[[0 for i in range(4)] for w in range(4)]

goal=[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]

path={}

def left(lst,row):
	newstate=copy.deepcopy(lst)
	temp=newstate[row][0]
	for i in range(3):
		newstate[row][i]=newstate[row][i+1]
	newstate[row][3]=temp
	return newstate

def right(lst,row):
	newstate=copy.deepcopy(lst)
	temp=newstate[row][-1]
	for i in range(3,0,-1):
		newstate[row][i]=newstate[row][i-1]
	newstate[row][0]=temp
	return newstate

def up(lst,col):
	newstate=copy.deepcopy(lst)
	temp=newstate[0][col]
	for i in range(3):
		newstate[i][col]=newstate[i+1][col]
	newstate[3][col]=temp
	return newstate

def down(lst,col):
	newstate=copy.deepcopy(lst)
	temp=newstate[-1][col]
	for i in range(3,0,-1):
		newstate[i][col]=newstate[i-1][col]
	newstate[0][col]=temp
	return newstate


def calculate_cost(state):
	count=0
	for i in range(4):
		for j in range(4):
			if (i*4+j+1) != state[i][j]:
				count += 1;
	return count/4.0

def expand_node(state,count):
	for i in range(4):
		newstateL=copy.deepcopy(left(state,i))
		move='L'+str(i)
		costL=calculate_cost(newstateL)+count
		dataL=(newstateL,move,count,state)
		left_tuple=(costL,dataL)
		#print left_tuple
		frontier.put(left_tuple)
	
	for j in range(4):
		newstateR=copy.deepcopy(right(state,j))
		move='R'+str(j)
		cost=calculate_cost(newstateR)+count
		dataR=(newstateR,move, count,state)
		right_tuple=(cost,dataR)
		#print right_tuple
		frontier.put(right_tuple)
	
	for k in range(4):
		newstateU=copy.deepcopy(up(state,k))
		move='U'+str(k)
		cost=calculate_cost(newstateU)+count
		dataU=(newstateU,move,count,state)
		up_tuple=(cost,dataU)
		#print up_tuple
		frontier.put(up_tuple)
	
	for l in range(4):
		newstateD=copy.deepcopy(down(state,l))
		move='D'+str(l)
		cost=calculate_cost(newstateD)+count
		dataD=(newstateD,move,count,state)
		down_tuple=(cost,dataD)
		#print down_tuple
		frontier.put(down_tuple)

def add_to_path(node):
	nodecopy= copy.deepcopy(node)
	parent_list=[]
	parent_list.append(nodecopy[1][3])
	parent_list.append(nodecopy[1][1])
	#print parent_list
	newkey=''
	newkey=''.join(str(e) for e in nodecopy[1][0])
	#print newkey
	path[newkey]=parent_list
	#print path


def print_path(node):
	stack=[]
	parent=[]
	nodecopy= copy.deepcopy(node)
	findkey=''.join(str(e) for e in nodecopy[1][0])
	#print findkey
	while (1):
		parent=path[findkey]
		if parent[1]==0:
			break 
		stack.append(parent[1])
		findkey=''
		findkey= ''.join(str(e) for e in parent[0])
	for i in reversed(stack):
		print i + "\t",
	

def Astar(initial,goal):
	if initial==goal:
		print "goal state is initial state only.. So, No move Required"
		return 0
	first=(initial,0,0,"NULL")
	frontier.put((0,first))
	while(not frontier.empty()):
		full_node=frontier.get()
		add_to_path(full_node)
		if full_node[1][0]==goal:
			print "Initaial State:  ", matrix ,"\n\n"	
			print_path(full_node)
			print "\n\n"
			print  "Goal State:  " , goal , "\n\n"
			return 0
		expand_node(full_node[1][0],full_node[1][2]+1)
	if frontier.empty():
		print " No Solution Exist "

with open(filename,"r") as myfile:
	input_numbers= myfile.readlines()
	row=0
	for line in input_numbers:
		numbers= line.split()
		col=0
		for num in numbers:
			matrix[row][col]=int(numbers[col])
			col = col + 1
		row = row + 1


Astar(matrix,goal)

