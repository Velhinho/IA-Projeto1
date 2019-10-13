import math
import pickle
import time


class Node:
  def __init__(self, transport_list):
    self.state = "undiscovered"
    self.parent = -1
    self.adjacency_list = self.add_adj_list(transport_list)
    self.transport_list = transport_list
  
  def add_adj_list(self, transport_list):
    adjacency_list = []
    for transport_tupple in transport_list:
      adjacency_list.append(transport_tupple[1])

    return adjacency_list

  def get_state(self):
    return self.state

  def set_state(self, new_state):
    self.state = new_state
    
  def get_parent(self):
    return self.parent

  def set_parent(self, new_parent):
    self.parent = new_parent

  def get_adjacency_list(self):
    return self.adjacency_list

  def get_transport_list(self):
    return self.transport_list


class SearchProblem:

  def __init__(self, goal, model, auxheur = []):
    self.goal = goal  # Goal position
    
    # Adjacency list of nodes of the graph
    # list of nodes has [transport, next_node]
    self.model = model    

    self.auxheur = auxheur  # Map coordenates of each node
    return

  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf]):
    # init = initial position

    graph = self.make_graph()
    
    return []

  def make_graph(self):
    graph = []
    for transport_list in self.model:
      node = Node(transport_list)
      graph.append(node)
    
    graph.pop(0)  # first node is empty
    return graph