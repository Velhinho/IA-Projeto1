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

  def get_node_from_vertex(self, vertex):
    position = vertex[1]
    return self.graph[position]

  def get_node_from_position(self, position):
    return self.graph[position]

  def enough_tickets(self, parent_node, next_vertex):
    # Check if enough tickets to go to next vertex
    transport = next_vertex[0]
    current_tickets = parent_node.get_ticket_list()
    return current_tickets[transport] - 1 > 0

  def take_ticket(self, parent_node, child_node, next_vertex):
    # Take away the ticket necessary to go from parent to child
    # Child_node knows which transport to take from parent_node
    transport = next_vertex[0]
    current_tickets = parent_node.get_ticket_list().copy()
    current_tickets[transport] -= 1
    child_node.set_parent_transport(transport)
    return current_tickets

  def bfs(self, start_position, end_position, tickets):
    start = self.get_node_from_position(start_position)
    end = self.get_node_from_position(end_position)
    start.set_state("discovered")
    start.set_parent(None)
    start.set_ticket_list(tickets)

    queue = []
    queue.append(start)

    while len(queue) > 0:
      parent_node = queue.pop(0)

      for next_vertex in parent_node.get_transport_list():
        child_node = self.get_node_from_vertex(next_vertex)

        if self.enough_tickets(parent_node, next_vertex):
          if child_node.get_state() == "undiscovered":
            child_node.set_state("discovered")
            child_node.set_parent(parent_node)
            current_tickets = self.take_ticket(parent_node, child_node, next_vertex)
            child_node.set_ticket_list(current_tickets)
            queue.append(child_node)

    return self.find_path(start, end)

  def find_path(self, start, end):

    if start.get_position() == end.get_position():
      return [start.get_position()]

    elif end.get_parent() == None:
      raise ValueError("No path")

    else:
      return self.find_path(start, end.get_parent()) + [end.get_position()]


class Node:
  def __init__(self, transport_list, position):
    self.state = "undiscovered"
    self.parent = None
    self.transport_list = transport_list
    self.ticket_list = None
    self.position = position
    self.parent_transport = None

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

    graph = Graph(self.model)
    # print(self.goal[0]) 4th test goal ??????????????/
    result = graph.bfs(init[0], self.goal[0], tickets)
    print(result)
    return []


def print_result(result_list):
  def has_play(indexes, lens):
      has_play = 3
      for i in range(len(indexes)):
        if indexes[i] == lens[i]:
          has_play -= 1

      return has_play > 0

  def get_play(result_list, indexes, lens):
    if not has_play(indexes, lens):
      return []

    transports = []
    positions = []

    for i in range(len(result_list)):
      result = result_list[i]
      limit = lens[i]
      idx = indexes[i]
      
      transports.append(result[idx][0])
      positions.append(result[idx][1])
      
      if idx < limit:
        idx += 1

  final_print = []
  lens = []
  indexes = []
  for r in result_list:
    lens.append(len(r))
    indexes.append(0)

  while(True):
    play = get_play(result_list, indexes, lens)

    if len(play) == 0:
      break

    final_print.append(play)