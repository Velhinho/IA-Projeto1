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
    self.f = math.inf
    self.g = math.inf
    self.h = math.inf
    self.x = 0
    self.y = 0
    
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

class NodePQueue:
  def __init__(self):
    self.queue = []

  def put(self, node):
    self.queue.append(node)

  def isEmpty(self):
    return len(self.queue) == 0

  def node_exists(self, node):
    for item in self.queue:
      if item.position == node.position:
        return True
    return False

  def get(self):
    #priority is minimum f value
    min = 0
    for i in range(len(self.queue)):
      if self.queue[i].f < self.queue[min].f:
        min = i
    return self.queue.pop(min)


class SearchProblem:

  def __init__(self, goal, model, auxheur = []):
    self.goal = goal  # Goal position
    
    # Adjacency list of nodes of the graph
    # list of nodes has [transport, next_node]
    self.model = model    

    self.auxheur = auxheur  # Map coordenates of each node
    return

  def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False):
    # init = initial position

    graph = self.make_graph()
    start_node = graph[init[0]]
    goal_node = graph[self.goal[0]]
    result = self.bfs(graph, start_node, goal_node)
    
    asd = []
    for node in result:
      print(node.get_position())
    print(asd)
    result2 = self.astar(graph, start_node, goal_node)
    for node in result2:
      print(node.get_position())
    print(asd)
    return []

  def make_graph(self):
    graph = []
    position = 0
    
    for transport_list in self.model:
      node = Node(transport_list, position)
      node.x = self.auxheur[position - 1][0]
      node.y = self.auxheur[position - 1][1]
      graph.append(node)
      position += 1
    
    return graph


  def find_path(self, graph, start, end):

      if start.get_position() == end.get_position():
        return [start]

      elif end.get_parent() == None:
        return []

      else:
        return self.find_path(graph, start, end.get_parent()) + [end]

  def astar(self, graph, start, end):

    openList = NodePQueue()
    closedList = []

    #heuristic value for every node
    for node in graph:
      deltaX = node.x - end.x
      deltaY = node.y - end.y
      node.h = deltaX ** 2 + deltaY ** 2

    graph[start.get_position()].f = 0
    graph[start.get_position()].g = 0
    openList.put(start)

    while not openList.isEmpty():
      current_node = openList.get()
      closedList.append(current_node)

      #end
      if current_node.position == end.position:
        return self.find_path(graph, start, end)

      for neighbor_pos in current_node.adjacency_list:
        if graph[neighbor_pos] in closedList:
          continue

        #step cost = 1
        tentative_g_score = current_node.g + 1

        if tentative_g_score < graph[neighbor_pos].g:
          #new g value is better, update costs
          graph[neighbor_pos].set_parent(current_node)
          graph[neighbor_pos].g = tentative_g_score
          graph[neighbor_pos].f = graph[neighbor_pos].g + graph[neighbor_pos].h

          if not openList.node_exists(graph[neighbor_pos]):
            openList.put(graph[neighbor_pos])

    return -1

  def bfs(self, graph, start, end):
  
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
    
    return self.find_path(graph, start, end)