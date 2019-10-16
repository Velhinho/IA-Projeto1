import math
import pickle
import time

class Graph:
  def __init__(self, model):
    self.graph = []
    position = 0

    for transport_list in model:
      node = Node(transport_list, position)
      self.graph.append(node)
      position += 1

  def get_node(self, position):
    return self.graph[position]

  def bfs(self, start_position, end_position):
    start = self.get_node(start_position)
    end = self.get_node(end_position)

    start.set_state("discovered")
    start.set_parent(None)
    queue = []
    queue.append(start)

    while len(queue) > 0:
      node_a = queue.pop(0)
      for vertex in node_a.get_adjacency_list():
        node_b = self.get_node(vertex)

        if node_b.get_state() == "undiscovered":
          node_b.set_state("discovered")
          node_b.set_parent(node_a)
          queue.append(node_b)

        node_a.set_state("expanded")

    return self.find_path(start, end)

  def find_path(self, start, end):

    if start.get_position() == end.get_position():
      return [start]

    elif end.get_parent() == None:
      raise ValueError

    else:
      return self.find_path(start, end.get_parent()) + [end]


class Node:
  def __init__(self, transport_list, position):
    self.state = "undiscovered"
    self.parent = None
    self.adjacency_list = self.add_adj_list(transport_list)
    self.transport_list = transport_list
    self.position = position
    
  def add_adj_list(self, transport_list):
    adjacency_list = []
    for transport_tuple in transport_list:
      adjacency_list.append(transport_tuple[1])

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

  def get_position(self):
    return self.position


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

    graph = Graph(self.model)
    # print(self.goal[0]) 4th test goal ??????????????/
    result = graph.bfs(init[0], self.goal[0])
    
    asd = []
    for node in result:
      asd.append(node.get_position())
    print(asd)

    return []
