import math
import pickle
import time


class Node:
  def __init__(self, adjacency):
    self.state = "undiscovered"
    self.parent = -1
    self.adjacency = adjacency


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

    make_graph(self.model)

    return []

  def make_graph(model):
    graph = []
    for adjacency in model:
      node = Node()


  def bfs(graph, start):
    for vertex_u in graph:

    
