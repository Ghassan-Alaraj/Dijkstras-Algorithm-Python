# imports
from copy import copy
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from itertools import combinations


def insertion_sort(A):
	''' Sort array A into ascending order using insertion sort.
		
		Parameters
		----------
		A : array
		    Array of values to be sorted in-place.
			
		Returns
		-------
		inds : array
			An index table for A.
		
		Notes
		-----
		Index table for sort constructed by applying the same sort operations
		to INDS that are applied to A.
		
	'''

	#copy A to not destroyed
	A_copy = copy(A)

	#insertion sort implimtation from notebook
	n = len(A)
	for j in range(1,n):
		key = A[j]
		i = j-1
		while i > -1:
			if not (A[i] > key):
				break
			A[i+1] = A[i]
			i -= 1
		A[i+1] = key
	
	#return index table
	indes = []
	indes = [A_copy.index(i) for i in A]

	return indes

def dijkstra(network, source_name, destination_name):
	''' Find shortest path between source and destination nodes in network.
	
		Parameters
		----------
		network : Network
			Network object containing information about arcs and nodes. Refer to Network class below.
		source_name : string
			Name of node object where path begins.
		destination_name : string
			Name of node object where path terminates.
			
		Returns
		-------
		distance : float
			Shortest distance between source and destination.
		shortest_path : list
			List of node NAMES that gives the route of the shortest path.
	
		Notes
		-----
		Node objects have the attribute 'value'.
		Network objects have the method get_node().
	'''
	# get node objects corresponding to input names
	destination = network.get_node(destination_name)
	source = network.get_node(source_name)
	# assign all nodes in the network a very large tentative distance
	for node in network.nodes:
		node.value = [float('Inf'), ]
	# assign source node a zero tentative distance and set as the current node
	network.get_node(source_name).value = [0, ]
	current_node = network.get_node(source_name)
	# create the set of unvisited nodes
	unvisited = set([nd.name for nd in network.nodes])
	
	
	# begin looping over nodes in the unvisited set
	keep_checking = True

	while keep_checking:
		vals = []

		# check tentative distances to linked nodes and assign 
		for arc in current_node.arcs_out:
			if arc.weight + arc.from_node.value[0] < arc.to_node.value[0]:
				arc.to_node.value = [arc.weight + arc.from_node.value[0], arc.from_node]
		# remove current node from unvisited set 
		#if desintation is not accessable from source, then return inf and empty array
		try:
			unvisited.remove(current_node.name)
		except KeyError:
			return float('Inf'), []
		# get next node - member of unvisited set with smallest tentative distance
		
		#collect all values, pass them to the insertion_sort() function to find index of smallest value
		#that becomes the current node
		for nd in network.nodes:
			vals.append(nd.value[0])

		indes = insertion_sort(vals)
		#update current node
		for i in indes:
			if network.nodes[i].name in unvisited:
				current_node = network.nodes[i]
				break
		

		# check exit conditions
		if destination_name not in unvisited:
			keep_checking = False

	
	# Final Step: extract and return path information
	# initialize
	path = [destination,]
	# create list of nodes
	while path[-1].name != source.name:
		path.append(path[-1].value[1])

	# create list of nodenames of shortest path
	shortest_path = [nd.name for nd in path][::-1]
	
	return destination.value[0], shortest_path
	
	
# --- for linked lists
class ListNode(object):
	'''A class with methods for node object.
	'''
	def __init__(self, value, pointer):
		'''Initialise a new node with VALUE and POINTER
		'''
		self.value = value
		self.pointer = pointer
		
	def __repr__(self):
		return "{}".format(self.value)
		
	def next(self):
		'''Returns the next node.
		'''
		return self.pointer
class LinkedList(object):
	'''A class with methods to implement linked list behavior.
	'''
	def __init__(self):
		'''Initialise an empty list.
		'''
		self.head = None
	def __repr__(self):
		'''Print out values in the list.
		'''
		# special case, the list is empty
		if self.head is None:
			return '[]'
		
		# print the head node
		ret_str = '['					   # open brackets
		node = self.head
		ret_str += '{}, '.format(node.value) # add value, comma and white space
		
		# print the nodes that follow, in order
		while node.pointer is not None:	 # stop looping when reach null pointer
			node = node.next()			  # get the next node
			ret_str += '{}, '.format(node.value)
		ret_str = ret_str[:-2] + ']'		# discard final white space and comma, close brackets
		return ret_str
	def append(self, value):
		'''Insert a new node with VALUE at the end of the list.
		'''
		# insert value at final index in list		
		self.insert(self.get_length(), value)
	def insert(self, index, value):
		'''Insert a new node with VALUE at position INDEX.
		'''
		# create new node with null pointer
		new_node = ListNode(value, None)
		
		# special case, inserting at the beginning
		if index == 0:
			# new node points to old head
			new_node.pointer = self.head
			# overwrite list head with new node
			self.head = new_node
			return
		
		# get the node immediately prior to index
		node = self.get_node(index-1)
		
		# logic to follow
		if node is None:					# special case, out of range
			print("cannot insert at index {:d}, list only has {:d} items".format(index, self.get_length()))
		elif node.next() is None:		   # special case, inserting as last node
			node.pointer = new_node
		else:
			# point new node to node after new node
			new_node.pointer = node.next()
			# node before new node points to new node
			node.pointer = new_node
	def pop(self, index):
		'''Delete node at INDEX and return its value.
		'''
		# special case, index == 0 (delete head)
		if index == 0:
			# popped value
			pop = self.head.value
			# set new head as second node
			self.head = self.head.next()
			return pop
		
		# get the node immediately prior to index
		node = self.get_node(index-1)
		
		# logic to follow
		if node is None:					# special case, out of range
			print("cannot access index {:d}, list only has {:d} items".format(index, self.get_length()))
			return None
		elif node.next() is None:		  # special case, out of range
			print("cannot access index {:d}, list only has {:d} items".format(index, self.get_length()))
			return None
		elif node.next().next() is None:  # special case, deleting last node
			# popped value
			pop = node.next().value
			
			# make prior node the last node
			node.pointer = None
		else:
			# popped value
			pop = node.next().value
			
			# set this nodes pointer so that it bypasses the deleted node
			node.pointer = node.next().next()
		
		return pop
	def delete(self,index):
		'''Delete node at INDEX.		
		'''
		# use pop method and discard output
		self.pop(index)
	def get_length(self):
		'''Return the length of the linked list.
		'''
		# special case, empty list
		if self.head is None:
			return 0
		
		# initialise counter
		length = 1
		node = self.head
		while node.pointer is not None:
			node = node.next()
			length += 1
			
		return length
	def get_node(self, index):
		'''Return the node at INDEX.
		'''
		# special case: index = -1, retrieve last node
		if index == -1:
			# begin at head
			node = self.head
			
			# loop through until Null pointer
			while node.pointer is not None:
				node = node.next()
			return node
		
		# begin at head, use a counter to keep track of index
		node = self.head
		current_index = 0
		
		# loop through to correct index
		while current_index < index:
			node = node.next()
			if node is None:
				return node
			current_index += 1
			# optional screen output
		return node
	def get_value(self, index):
		'''Return the value at INDEX.
		'''
		# get the node at INDEX
		node = self.get_node(index)
		
		# return its value (special case if node is None)
		if node is None:
			return None
		else: 
			return node.value

# --- for networks
class Node(object):
	def __init__(self):
		self.name = None
		self.value = None
		self.arcs_in = []
		self.arcs_out = []
	def __repr__(self):
		return "nd: {}".format(self.name)
class Arc(object):
	def __init__(self):
		self.weight=None
		self.to_node = None
		self.from_node = None
	def __repr__(self):
		if self.to_node is None:
			to_nd = 'None'
		else:
			to_nd = self.to_node.name
		if self.from_node is None:
			from_nd = 'None'
		else:
			from_nd = self.from_node.name
		return "arc: {}->{}".format(from_nd, to_nd)
class NetworkError(Exception):
	'''An error to raise when violations occur.
	'''
	pass
class Network(object):
	''' Basic network class.
	'''
	def __init__(self):
		self.nodes = []
		self.arcs = []
	
	def __repr__(self):
		return ("ntwk(" + ''.join([len(self.nodes)*'{},'])[:-1]+")").format(*[nd.name for nd in self.nodes])
	
	def add_node(self, name, value=None):
		'''Adds a Node with NAME and VALUE to the network.
		'''
		# check node names are unique
		network_names = [nd.name for nd in self.nodes]
		if name in network_names:
			raise NetworkError("Node with name \'{}\' already exists.".format(name))
		
		# new node, assign values, append to list
		node = Node()
		node.name = name
		node.value = value
		self.nodes.append(node)
		
	def join_nodes(self, node_from, node_to, weight):
		'''Adds an Arc joining NODE_FROM to NODE_TO with WEIGHT.
		'''
		# new arc
		arc = Arc()
		arc.weight = weight
		arc.to_node = node_to
		arc.from_node = node_from
		# append to list
		self.arcs.append(arc)
		# make sure nodes know about arcs
		node_to.arcs_in.append(arc)
		node_from.arcs_out.append(arc)

	def read_network(self, filename):
		'''Read data from FILENAME and construct the network.
		'''
		# open network file
		fp = open(filename, 'r')
		
		# get first line
		ln = fp.readline().strip()
		while ln is not '':
			# node name
			ln2 = ln.split(',')
			from_node_name = ln2[0]
			arcs = ln2[1:]
			# if node doesn't exist, add to network
			try:
				self.get_node(from_node_name)
			except NetworkError:
				self.add_node(from_node_name)
			# get from node
			from_node = self.get_node(from_node_name)
			
			# read arcs
			for arc in arcs:
				to_node_name, weight = arc.split(';')
				weight = int(weight)
				
				# check if to_node defined
				try:
					self.get_node(to_node_name)
				except NetworkError:
					self.add_node(to_node_name)
				
				# get to node
				to_node = self.get_node(to_node_name)
				
				# add arc
				self.join_nodes(from_node, to_node, weight)
			
			# get next line
			ln = fp.readline().strip()
			
		fp.close()
	
	def get_node(self, name):
		''' Loops through the list of nodes and returns the one with NAME.
		
			Raises NetworkError if node does not exist.
		'''
		for node in self.nodes:
			if node.name == name:
				return node
		
		raise NetworkError('Node \'{}\' does not exist.'.format(name))

def main():
    island = Network()
    island.read_network(filename='network_final.txt')
    #nodes and corresponding island
    # T ; Taiwan
    # CI ; Caroline Islands
    # P ; palau
    # D ; Bismack sea
    # NM ; Sorong
    # HI ; Tarawa
    # V ; Vanuata
    # CT ; Cairns
    # SC ; Brisbane
    # F ; Fiji
    # To ; Tonga
    # CoI ; Cook Islands
    # S ; Samoa
    # FP ; French polynesia
    # PI ; Pitcarin Islands
    # IoH ; Islands of Hawii
    # H ; Hokianga
    # find shortest path betweem Taiwan and Hokianga

    #find shorest path
    time, shortest_path = dijkstra(network=island, source_name= 'T', destination_name= 'H')

    print('T - H')
    print(time, shortest_path)

    #to find all combinations of nodes we compute 17 choose 2. 
    names = [nd.name for nd in island.nodes]
    comb = combinations(names, 2)

    #compute shorest distance between all nodes
    paths = []
    distances = []
    for i in comb:
        distance, shortest_path = dijkstra(network=island, source_name= i[0], destination_name= i[1])
        paths.append(shortest_path)
        distances.append(distance)

    #remove infs and [] i.e. inaccessible routes
    distances = [i for i in distances if i != float('Inf')]
    paths = [i for i in paths if i != []]

    #find index of max in the network
    i_max = np.argmax(distances)
    #print results using said index
    print('longest path in the network')
    print(distances[i_max],paths[i_max])

if __name__ == "__main__":
    #Author: Ghassan Al-A'raj
    main()