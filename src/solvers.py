import os
import z3
from postman_problems.solver import cpp

from data import *

def calculate_basic_metrics():
  graph = construct_graph()
  degrees = {
    node: nx.degree(graph, node)
    for node in graph.nodes
  }
  min_node = min(degrees, key = degrees.get)
  max_node = max(degrees, key = degrees.get)

  return {
    # add 5 because I remove 5 vertices (ISL, IRL, GBR, MLT, CYP)
    # to get graph G from G*, but I need count |V| for G*
    "vertices_count": graph.number_of_nodes() + 5,
    # likewise add 1 removed edge (IRL - GBR)
    "edges_count": graph.number_of_edges() + 1,  
    "min_degree": degrees[min_node],
    "max_degree": degrees[max_node],
    "radius": nx.radius(graph),
    "diameter": nx.diameter(graph),
    # cycle with length 2 cannot exists, but we can find cycle
    # with length 3, in example FRA -> ESP -> AND -> FRA
    "girth": 3,
    "center": [
      node
      for node in graph.nodes
      if nx.eccentricity(graph, node) == nx.radius(graph)
    ],
    "vertex_connectivity": nx.node_connectivity(graph),
    "edge_connectivity": nx.edge_connectivity(graph),
  }

def minimum_vertex_coloring():
  solver = z3.Optimize()
  constraints = []

  k = z3.Int("k")
  vertices = {v : z3.Int(v.name) for v in VERTICES}

  for v in vertices.values():
    constraints.append(z3.And(0 <= v, v < k))

  for v1 in VERTICES:
    for v2 in VERTICES:
      if v1.is_adjacent(v2):
        constraints.append(vertices[v1] != vertices[v2])

  solver.add(constraints)
  solver.minimize(k)
  solver.check()
  model = solver.model()

  for v in VERTICES:
    v.options = {
      "vertex_color": int(str(model[vertices[v]]))
    }
  for e in EDGES:
    e.options = {}
  return VERTICES, EDGES

def minimum_edge_coloring():
  solver = z3.Optimize()
  constraints = []

  k = z3.Int("k")
  edges = {e : z3.Int(e.name) for e in EDGES}

  for e in edges.values():
    constraints.append(z3.And(0 <= e, e < k))

  for e1 in EDGES:
    for e2 in EDGES:
      if e1.is_adjacent(e2):
        constraints.append(edges[e1] != edges[e2])

  solver.add(constraints)
  solver.minimize(k)
  solver.check()
  model = solver.model()

  for v in VERTICES:
    v.options = {}
  for e in EDGES:
    e.options = {
      "edge_color": int(str(model[edges[e]]))
    }
  return VERTICES, EDGES


def maximum_clique():
  solver = z3.Optimize()
  constraints = []

  k = z3.Int("k")
  vertices = {v: z3.Bool(v.name) for v in VERTICES}

  for v1 in VERTICES:
    for v2 in VERTICES:
      if v1.name != v2.name:
        constraints.append(z3.Implies(
          z3.And(vertices[v1], vertices[v2]),
          v1.is_adjacent(v2)
        ))
  constraints.append(z3.Sum([z3.If(v, 1, 0) for v in vertices.values()]) == k)

  solver.add(constraints)
  solver.maximize(k)
  solver.check()
  model = solver.model()

  for v in VERTICES:
    v.options = { "choose_vertex": bool(model.eval(vertices[v])) }
  for e in EDGES:
    e.options = { "choose_edge": False }
    for v in VERTICES:
      if v.name == e.begin and not v.options["choose_vertex"]:
        break
      if v.name == e.end and not v.options["choose_vertex"]:
        break
    else:
      e.options = { "choose_edge": True }
      
  return VERTICES, EDGES

def maximum_independent_set():
  solver = z3.Optimize()
  constraints = []
  
  k = z3.Int("k")
  vertices = {v: z3.Bool(v.name) for v in VERTICES}

  for v1 in VERTICES:
    for v2 in VERTICES:
      if v1.is_adjacent(v2):
        constraints.append(z3.Not(z3.And(vertices[v1], vertices[v2])))
  
  constraints.append(z3.Sum([z3.If(v, 1, 0) for v in vertices.values()]) == k)

  solver.add(constraints)
  solver.maximize(k)
  solver.check()
  model = solver.model()

  for v in VERTICES:
    v.options = { "choose_vertex": bool(model.eval(vertices[v])) }
  for e in EDGES:
    e.options = {}
      
  return VERTICES, EDGES

def maximum_matching():
  solver = z3.Optimize()
  constraints = []
  
  k = z3.Int("k")
  edges = {e: z3.Bool(e.name) for e in EDGES}

  for e1 in EDGES:
    for e2 in EDGES:
      if e1.is_adjacent(e2):
        constraints.append(z3.Not(z3.And(edges[e1], edges[e2])))
  
  constraints.append(z3.Sum([z3.If(e, 1, 0) for e in edges.values()]) == k)

  solver.add(constraints)
  solver.maximize(k)
  solver.check()
  model = solver.model()

  for v in VERTICES:
    v.options = {}
  for e in EDGES:
    e.options = { "choose_edge": bool(model.eval(edges[e])) }
      
  return VERTICES, EDGES

def minimum_vertex_cover():
  solver = z3.Optimize()
  constraints = []
  
  k = z3.Int("k")
  vertices = {v.name: z3.Bool(v.name) for v in VERTICES}

  for e in EDGES:
    constraints.append(z3.Or(
      vertices[e.begin],
      vertices[e.end]
    ))
  
  constraints.append(z3.Sum([z3.If(v, 1, 0) for v in vertices.values()]) == k)

  solver.add(constraints)
  solver.minimize(k)
  solver.check()
  model = solver.model()

  for v in VERTICES:
    v.options = { "choose_vertex": bool(model.eval(vertices[v.name])) }
  for e in EDGES:
    e.options = {}
      
  return VERTICES, EDGES

def minimum_edge_cover():
  solver = z3.Optimize()
  constraints = []
  
  k = z3.Int("k")
  edges = {e: z3.Bool(e.name) for e in EDGES}

  for v in VERTICES:
    constraints.append(z3.Or([
      edges[e]
      for e in EDGES
      if e.begin == v.name or e.end == v.name
    ]))
  
  constraints.append(z3.Sum([z3.If(e, 1, 0) for e in edges.values()]) == k)

  solver.add(constraints)
  solver.minimize(k)
  solver.check()
  model = solver.model()

  for v in VERTICES:
    v.options = {}
  for e in EDGES:
    e.options = { "choose_edge": bool(model.eval(edges[e])) }
      
  return VERTICES, EDGES

# still too slow, don't use it
# I prove minimality of circuit in other way
# def minimum_vertex_walk():
#   solver = z3.Solver()
#   constraints = []
  
#   k = 51 # choose the number of vertices in walk
#   constraints = []
#   walk = [z3.Int(f"v{i}") for i in range(k)]

#   # convert MATRIX to z3.Array
#   adjacent_list = z3.Array("adjacent_list", z3.IntSort(), z3.BoolSort())
#   idx = 0
#   for v1 in VERTICES:
#     for v2 in VERTICES:
#       adjacent_list = z3.Store(adjacent_list, idx, v1.is_adjacent(v2))
#       idx += 1

#   for i in range(k):
#     constraints.append(z3.And(0 <= walk[i], walk[i] < len(VERTICES)))
#   for i in range(k - 1):
#     constraints.append(
#       z3.Select(adjacent_list, walk[i] * len(VERTICES) + walk[i + 1]) == True
#     )
#   for i in range(len(VERTICES)):
#     constraints.append(z3.Sum([z3.If(v == i, 1, 0) for v in walk]) > 0)

#   constraints.append(walk[0] == 0)
#   constraints.append(walk[0] == walk[-1])

#   solver.add(constraints)
#   solver.check()
#   model = solver.model()

#   return " ".join([VERTICES[int(str(model[v]))].name for v in walk])

def minimum_edge_walk():
  temp_file = "__temp_matrix__.csv"

  with open(temp_file, "w", encoding="utf8") as file:
    file.write("node1,node2,trail,distance\n")
    for e in EDGES:
      file.write(f"{e.begin},{e.end},{e.name},1\n")

  circuit, _ = cpp(edgelist_filename=temp_file)
  os.remove(temp_file)
  return "\n".join(list(map(lambda e: f"{e[0]}-{e[1]}", circuit)))

def minimum_spanning_tree(mst_edges):
  for v in VERTICES:
    v.options = {}
  
  for e in EDGES:
    in_mst = False
    for pair in mst_edges:
      if e.is_equal_to_pair(pair):
        in_mst = True
        break

    e.options = { "draw_weight": in_mst, "choose_edge": in_mst }
    
  return VERTICES, EDGES

def centroid(mst_edges):
  for e in EDGES:
    for pair in mst_edges:
      if e.is_equal_to_pair(pair):
        e.options = { "in_mst": True }
        break
    else:
      e.options = { "in_mst": False }

  def dfs(vertex, parent):
    branch_weight = 0
    for edge in EDGES:
      if not edge.have_vertex(vertex) or not edge.options["in_mst"]:
        continue
      following = edge.other_vertex(vertex)
      if following == parent:
        continue

      branch_weight += edge.weight + dfs(following, vertex)
    return branch_weight

  for v in VERTICES:
    v.options["max_branch_weight"] = 0

    for neighbour in VERTICES:
      if not v.is_adjacent(neighbour):
        continue
      v.options["max_branch_weight"] = max(
        v.options["max_branch_weight"],
        dfs(neighbour.name, v.name)
      )

  centroid = min(VERTICES, key = lambda v: v.options["max_branch_weight"])
  best_branch_weight = centroid.options["max_branch_weight"]

  output = "Centroid: "
  for v in VERTICES:
    if v.options["max_branch_weight"] == best_branch_weight:
      output += f"{v.name} "
  return output

def prufer_encode(mst):
  mapping = {}
  for i, v in enumerate(VERTICES):
    mapping[v.name] = i

  mst = nx.relabel_nodes(mst, mapping)
  code = nx.to_prufer_sequence(mst)

  return ", ".join([VERTICES[i].name for i in code])
