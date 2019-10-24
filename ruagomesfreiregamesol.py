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

  def get_node_list(self):
    return iter(self.graph)

  def get_node_from_vertex(self, vertex):
    position = vertex[1]
    return self.graph[position]

  def get_node_from_position(self, position):
    return self.graph[position]

  def enough_tickets(self, parent_node, next_vertex):
    # Check if enough tickets to go to next vertex
    transport = next_vertex[0]
    current_tickets = parent_node.get_ticket_list()
    return current_tickets[transport] > 0

  def take_ticket(self, parent_node, child_node, next_vertex):
    # Take away the ticket necessary to go from parent to child
    # Child_node knows which transport to take from parent_node
    transport = next_vertex[0]
    current_tickets = parent_node.get_ticket_list().copy()
    current_tickets[transport] -= 1
    child_node.set_parent_transport(transport)
    return current_tickets

class Node:
  def __init__(self, transport_list, position):
    self.state = "undiscovered"
    self.parent = None
    self.transport_list = transport_list
    self.ticket_list = None
    self.position = position
    self.parent_transport = None
    self.distance = None

  def get_state(self):
    return self.state

  def set_state(self, new_state):
    self.state = new_state
    
  def get_parent(self):
    return self.parent

  def set_parent(self, new_parent):
    self.parent = new_parent

  def get_transport_list(self):
    return self.transport_list

  def get_ticket_list(self):
    return self.ticket_list

  def set_ticket_list(self, ticket_list):
    self.ticket_list = ticket_list

  def get_position(self):
    return self.position

  def get_parent_transport(self):
    return self.parent_transport

  def set_parent_transport(self, parent_transport):
    self.parent_transport = parent_transport

  def get_distance(self):
    return self.distance

  def set_distance(self, distance):
    self.distance = distance

  def has_neighbor(self, neighbor):
    neighbor_pos = neighbor.get_position()
    for next_vertex in self.get_transport_list():
      if next_vertex[1] == neighbor_pos:
        return True
    return False

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

    graph_list, start_list, end_list = make_graphs(init, self.goal, self.model)
    result_list = threefs(graph_list, start_list, end_list, tickets)
    fix_paths(graph_list, result_list)
    print_list = get_print_list(result_list)
    return []


def make_graphs(start_position_list, end_position_list, model):
  graph_list = []
  start_list = []
  end_list = []

  for start, end in zip(start_position_list, end_position_list):
    graph = Graph(model)
    graph_list.append(graph)

    start_node = graph.get_node_from_position(start)
    start_list.append(start_node)
    end_node = graph.get_node_from_position(end)
    end_list.append(end_node)
  
  return (graph_list, start_list, end_list)

def threefs(graph_list, start_list, end_list, ticket_list):
  result_list = []
  for graph, start, end in zip(graph_list, start_list, end_list):
    result = bfs(graph_list, graph, start, end, ticket_list)
    result_list.append(result)
  return result_list

def bfs(graph_list, current_graph, start, end, ticket_list):
  start.set_state("discovered")
  start.set_parent(None)
  start.set_distance(0)
  start.set_ticket_list(ticket_list)
  queue = []
  queue.append(start)

  while len(queue) > 0:
    parent_node = queue.pop(0)
    current_distance = parent_node.get_distance()

    for next_vertex in parent_node.get_transport_list():
      child_node = current_graph.get_node_from_vertex(next_vertex)
      
      if (not current_graph.enough_tickets(parent_node, next_vertex)) \
          or taken_spot(graph_list, current_graph, current_distance, next_vertex):
        continue

      elif child_node.get_state() == "undiscovered":
        child_node.set_state("discovered")
        child_node.set_parent(parent_node)
        child_node.set_distance(current_distance + 1)
        current_tickets = current_graph.take_ticket(parent_node, child_node, next_vertex)
        child_node.set_ticket_list(current_tickets)
        queue.append(child_node)
      
      parent_node.set_state("expanded")
  
  return find_path(start, end)

def taken_spot(graph_list, current_graph, current_distance, next_vertex):
    for graph in graph_list:
        if graph == current_graph:
            continue

        node = current_graph.get_node_from_vertex(next_vertex)
        if node.get_state() == "taken" and node.get_distance() == current_distance:
          return True
    return False

def find_path(start, end):
  if start.get_position() == end.get_position():
    start.set_state("taken")
    return [start]

  elif end.get_parent() == None:
    raise ValueError("No path")

  else:
    end.set_state("taken")
    return find_path(start, end.get_parent()) + [end]

def fix_paths(graph_list, result_list):
  max_len = max(len(x) for x in result_list)
  for graph, result in zip(graph_list, result_list):
    extend_path(graph_list, graph, result, max_len)

def extend_path(graph_list, current_graph, result, max_len):
  diff = len(result) - max_len
  while diff < 0:    
    if diff % 2 == 1:
      fix_odd_path(graph_list, current_graph, result)
    else:
      fix_even_path(graph_list, current_graph, result, max_len)
    diff = len(result) - max_len

def fix_odd_path(graph_list, current_graph, result):
  final_node = get_node_from_result(current_graph, result, -1)
  penultimate_node = get_node_from_result(current_graph, result, -2)
  
  # Search adjacent vertices for a not yet taken vertex
  for next_vertex in final_node.get_transport_list():
    neighbour_node = current_graph.get_node_from_vertex(next_vertex)
    if neighbour_node.get_state() != "taken" \
      and neighbour_node.has_neighbor(penultimate_node):
      extra_node = neighbour_node
  
  result.pop()
  result.append(extra_node)
  result.append(final_node)

def fix_even_path(graph_list, current_graph, result, max_len):
  final_pos = get_node_from_result(result, -1)
  final_node = current_graph.get_node_from_position(final_pos)

  # Search adjacent vertices for a not yet taken vertex
  for next_vertex in final_node.get_transport_list():
    neighbour_node = current_graph.get_node_from_vertex(next_vertex)
    if neighbour_node.get_state() != "taken":
      extra_node = neighbour_node
  
  while len(result) != max_len:
    result.append(extra_node)
    result.append(final_node)

def get_node_from_result(graph, result, index):
  return result[index]

def get_print_list(result_list):
  print_list = []
  for nodes in zip(*result_list):
    transport = []
    moves = []
    for node in nodes:
      transport.append(node.get_parent_transport())
      moves.append(node.get_position())
    print_list.append([transport, moves])
  return print_list

