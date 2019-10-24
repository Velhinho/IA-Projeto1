import math
import pickle
import time

class Graph:
  def __init__(self, model):
    self.graph = []
    position = 0
    self.model = model

    for transport_list in model:
      node = Node(transport_list, position)
      self.graph.append(node)
      position += 1

  def get_node(self, position):
    return self.graph[position]

  def get_graph_iter(self):
    return iter(self.graph)

  def bfs(self, start_position, end_position):
    start = self.get_node(start_position)
    end = self.get_node(end_position)

    start.set_state("discovered")
    start.set_parent(None)
    queue = []
    queue.append(start)

    while len(queue) > 0:
      node_parent = queue.pop(0)
      for vertex in node_parent.get_adjacency_list():
        node_child = self.get_node(vertex)

        if node_child.get_state() == "undiscovered":
          node_child.set_state("discovered")
          node_child.set_parent(node_parent)

          transport = node_parent.get_child_transport(node_child.get_position())
          node_child.set_parent_transport(transport)
          queue.append(node_child)

        if node_parent.get_position() == end.get_position():
          return self.find_path(start, end)

        node_parent.set_state("expanded")

    raise ValueError("bfs: couldn't find path")

  def find_path(self, start, end, occupied_nodes):

    occupied_nodes.append(end)

    if start.get_position() == end.get_position():
      return [[[], [start.get_position()]]]

    elif end.get_parent() == None:
      raise ValueError("No path")

    else:
      return self.find_path(start, end.get_parent(), occupied_nodes) + [[[end.get_parent_transport()], [end.get_position()]]]

  def astar(self, start_position, end_position, tickets, occupied_nodes):

    newgraph = Graph(self.model)
    start = newgraph.get_node(start_position)
    end = newgraph.get_node(end_position)

    openList = NodePQueue()
    closedList = []

    for node in newgraph.get_graph_iter():
      node.tickets = [math.inf, math.inf, math.inf]
      node.parent = {"transport": [], "parent_node": None}
      node.f = math.inf
      node.g = math.inf
      deltaX = node.x - end.x
      deltaY = node.y - end.y
      node.h = deltaX ** 2 + deltaY ** 2

    start.f = 0
    start.g = 0
    start.tickets = tickets
    openList.put(start)

    while not openList.isEmpty():
      current_node = openList.get()
      closedList.append(current_node)

      #end
      if current_node.position == end.position:
        return newgraph.find_path(start, end, occupied_nodes), current_node.tickets

      for neighbor_pos in current_node.get_adjacency_list():
        neighbor_node = newgraph.get_node(neighbor_pos)
        if neighbor_node in closedList:
          continue

        #step cost = 1
        tentative_g_score = current_node.g + 1

        if tentative_g_score < neighbor_node.g:
          #new g value is better, update costs
          transportList = current_node.get_child_transport(neighbor_pos)
          for transport in transportList:
            #not enough tickets for this transport, check other transports available
            if current_node.tickets[transport] == 0:
              continue
            neighbor_node.tickets[0] = current_node.tickets[0]
            neighbor_node.tickets[1] = current_node.tickets[1]
            neighbor_node.tickets[2] = current_node.tickets[2]
            neighbor_node.tickets[transport] -= 1
            neighbor_node.set_parent_transport(transport)       
            neighbor_node.set_parent(current_node)
            neighbor_node.g = tentative_g_score
            neighbor_node.f = neighbor_node.g + neighbor_node.h
            if not (openList.node_exists(neighbor_node) or self.node_is_occupied(neighbor_node, occupied_nodes)):
              openList.put(neighbor_node)

    raise ValueError("astar: couldn't find path")

  def node_is_occupied(self, node, nodeList):
    for item in nodeList:
      if item.g == node.g and item.position == node.position:
        return True
    return False

class Node:
  def __init__(self, transport_list, position):
    self.state = "undiscovered"
    self.parent = {"transport": [], "parent_node": None}

    # transport tuple [transport, next_position]
    self.adjacency_list = self.add_adj_list(transport_list)    
    self.transport_dict = self.add_transport_dict(transport_list)
    self.position = position
    self.f = math.inf
    self.g = math.inf
    self.h = math.inf
    self.x = 0
    self.y = 0
    self.tickets = [math.inf, math.inf, math.inf]
    
  def add_adj_list(self, transport_list):
    adjacency_list = []
    for transport_tuple in transport_list:
      adjacency_list.append(transport_tuple[1])
    return adjacency_list

  def add_transport_dict(self, transport_list):
    transport_dict = {}
    for transport_tuple in transport_list:
      position = str(transport_tuple[1])
      if position in transport_dict:
        transport_dict[position].append(transport_tuple[0])
      else:
        transport_dict[position] = [transport_tuple[0]]
    return transport_dict

  def get_state(self):
    return self.state

  def set_state(self, new_state):
    self.state = new_state
    
  def get_parent(self):
    return self.parent["parent_node"]

  def get_parent_transport(self):
    return self.parent["transport"]

  def set_parent(self, new_parent):
    self.parent["parent_node"] = new_parent

  def set_parent_transport(self, new_transport):
    self.parent["transport"] = new_transport

  def get_adjacency_list(self):
    return self.adjacency_list

  def get_child_transport(self, child_position):
    position = str(child_position)
    return self.transport_dict[position]

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
      if item.position == node.position and item.parent["transport"] == node.parent["transport"]:
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

    graph = Graph(self.model)
    
    # # print(self.goal[0]) 4th test goal ??????????????/
    # result = graph.bfs(init[0], self.goal[0])
    # print(result)

    # result2 = graph.astar(init[0], self.goal[0])
    # print(result2)


    occupied_nodes = []
    result1, newtickets1 = graph.astar(init[0], self.goal[0], tickets, occupied_nodes)

    if len(self.goal) == 1:
      return result1
    else:
      # print("occupied_nodes:")
      # for node in occupied_nodes:
      #   print(node.position)
      #   print(node.g)
      result2, newtickets2 = graph.astar(init[1], self.goal[1], newtickets1, occupied_nodes)
      # print("occupied_nodes:")
      # for node in occupied_nodes:
      #   print(node.position)
      #   print(node.g)
      result3, newtickets3 = graph.astar(init[2], self.goal[2], newtickets2, occupied_nodes)
      # print("occupied_nodes:")
      # for node in occupied_nodes:
      #   print(node.position)
      #   print(node.g)

      finalres = []
      max_result_length = max(len(result1), len(result2), len(result3))
      for i in range(0, max_result_length):
        finalres.append([])
      # self.extend_result(result1, max_result_length)
      # self.extend_result(result2, max_result_length)
      # self.extend_result(result3, max_result_length)
      result_list = []
      result_list.append(result1)
      result_list.append(result2)
      result_list.append(result3)

      print(result_list)
      self.fix_paths(result_list, occupied_nodes, graph)

      print(result_list)
      print(result_list[0])
      print(result_list[1])
      print(result_list[2])

      for index, item in enumerate(finalres):
        if index == 0:
          item.append([])
          goal_list = []
          goal_list.append(result1[0][1][0])
          goal_list.append(result2[0][1][0])
          goal_list.append(result3[0][1][0])
          item.append(goal_list)
          continue
        transportlist = []
        transportlist.append(result1[index][0][0])
        transportlist.append(result2[index][0][0])
        transportlist.append(result3[index][0][0])
        item.append(transportlist)
        goallist = []
        goallist.append(result1[index][1][0])
        goallist.append(result2[index][1][0])
        goallist.append(result3[index][1][0])
        item.append(goallist)

      print("final result:")
      print(finalres)
      return finalres


  def extend_result(self, result_list, new_length):
    last_result = result_list[-1]
    while len(result_list) < new_length:
      result_list.append(last_result)
    return

  def fix_paths(self, result_list, occupied_nodes, graph):
    max_length = max(len(result) for result in result_list)
    print(max_length)
    for result in result_list:
      i = len(result)
      print("new result")
      while i < max_length:
        time.sleep(0.5)
        print(i)
        if i % 2 == 1:
          print("got in uneven function")
          final_node = graph.get_node(result[-1][1][0])
          penultimate_node = graph.get_node(result[-2][1][0])
          common_positions = list(set(final_node.adjacency_list).intersection(penultimate_node.adjacency_list))
          if len(common_positions) == 0:
            print("ULTIMATE FAILURE")
            print(penultimate_node.position)
            print(final_node.position)
          gScore = penultimate_node.g + 1
          alternative_found = False
          for pos in common_positions:
            if alternative_found:
              print("found alternative, nice")
              break
            for node in occupied_nodes:
              if node.position == pos and node.g != gScore:
                transportUsed = penultimate_node.transport_dict[str(pos)]
                result.insert(len(result) - 1, [[transportUsed[0]], [pos]])
                last_transport = penultimate_node.transport_dict[str(final_node.position)]
                result[-1][0][0] = last_transport[0]
                alternative_found = True
                i += 1
                break
        if i == max_length:
          break
        final_node = graph.get_node(result[-1][1][0])
        gScore = final_node.g + 1
        print("final node position")
        print(final_node.position)
        print("final node adjacencylist")
        print(final_node.adjacency_list)
        for neighbor_pos in final_node.adjacency_list:
          neighbor = graph.get_node(neighbor_pos)
          transportUsed = final_node.transport_dict[str(neighbor_pos)]
          result.append([[transportUsed[0]], [neighbor_pos]])
          result.append([[transportUsed[0]], [final_node.position]])
          i += 2
          break
          # if neighbor.g != gScore:
          #   transportUsed = final_node.transport_dict[str(neighbor_pos)]
          #   result.append([[transportUsed], [neighbor_pos]])
          #   i += 2
          #   break
    return

