import math
import pickle
import time


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

    graph = self.make_graph()
    start_node = graph[init[0]]
    goal_node = graph[self.goal[0]]
    result = self.bfs(graph, start_node, goal_node)
    
    asd = []
    for node in result:
      print(node.get_position())
    print(asd)

    return []

  def make_graph(self):
    graph = []
    position = 0
    
    for transport_list in self.model:
      node = Node(transport_list, position)
      graph.append(node)
      position += 1
    
    return graph

  def bfs(self, graph, start, end):
    def find_path(graph, start, end):

      if start.get_position() == end.get_position():
        return [start]

      elif end.get_parent() == None:
        return []

      else:
        return find_path(graph, start, end.get_parent()) + [end]
  
    start.set_state("discovered")
    start.set_parent(None)

    queue = []
    queue.append(start)

    while len(queue) > 0:
      vertex_a = queue.pop(0)
      for vertex_b in vertex_a.get_adjacency_list():
        if graph[vertex_b].get_state() == "undiscovered":
          graph[vertex_b].set_state("discovered")
          graph[vertex_b].set_parent(vertex_a)
          queue.append(graph[vertex_b])
        
        vertex_a.set_state("expanded")
    
    return find_path(graph, start, end)