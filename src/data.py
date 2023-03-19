from collections import defaultdict
MATRIX = defaultdict(lambda: defaultdict(bool))

import networkx as nx

class Vertex:

  def __init__(self, name, position):
    self.name = name
    self.position = position
    self.options = {}
  
  def __hash__(self):
    return hash(self.name)

  def is_adjacent(self, other):
    return MATRIX[self.name][other.name]

class Edge:

  def __init__(self, begin, end, weight):
    self.begin = begin
    self.end = end
    self.weight = weight
    self.name = f"{begin}-{end}"
    self.options = {}
  
  def __hash__(self):
    return hash(self.name)

  def is_adjacent(self, other):
    if self.name == other.name:
      return False
    return self.begin == other.begin or self.begin == other.end \
      or self.end == other.begin or self.end == other.end
  
  def have_vertex(self, vertex):
    return self.begin == vertex or self.end == vertex
    
  def is_equal_to_pair(self, pair):
    return (self.begin == pair[0] and self.end == pair[1]) or \
      (self.begin == pair[1] and self.end == pair[0])
  
  def other_vertex(self, vertex):
    if vertex == self.begin:
      return self.end
    if vertex == self.end:
      return self.begin
    return None

VERTICES = [
  Vertex("ARM", (18.9, 04.0)), Vertex("ALB", (10.0, 02.4)), Vertex("AND", (04.5, 06.3)),
  Vertex("AUT", (09.5, 10.4)), Vertex("BLR", (14.0, 12.9)), Vertex("BEL", (04.5, 14.0)),
  Vertex("BIH", (10.8, 06.4)), Vertex("BGR", (15.5, 06.0)), Vertex("HRV", (09.2, 06.7)),
  Vertex("CZE", (10.4, 11.7)), Vertex("DNK", (08.2, 15.8)), Vertex("EST", (14.6, 15.4)),
  Vertex("FIN", (16.0, 19.0)), Vertex("FRA", (04.9, 10.9)), Vertex("DEU", (08.5, 13.5)),
  Vertex("GEO", (19.0, 05.7)), Vertex("GRC", (13.0, 03.0)), Vertex("HUN", (12.3, 09.5)),
  Vertex("ITA", (07.1, 06.0)), Vertex("XKX", (11.8, 05.2)), Vertex("LVA", (13.3, 16.0)),
  Vertex("LIE", (08.2, 11.0)), Vertex("LTU", (11.7, 16.5)), Vertex("LUX", (06.1, 12.9)),
  Vertex("MDA", (15.8, 09.6)), Vertex("MCO", (02.5, 10.0)), Vertex("MNE", (09.6, 04.0)),
  Vertex("NLD", (05.7, 15.0)), Vertex("MKD", (13.5, 05.0)), Vertex("NOR", (18.4, 16.8)),
  Vertex("POL", (09.6, 17.3)), Vertex("PRT", (01.0, 03.6)), Vertex("ROU", (15.3, 07.7)),
  Vertex("RUS", (16.6, 17.2)), Vertex("SMR", (07.8, 03.8)), Vertex("SRB", (12.9, 07.7)),
  Vertex("SVK", (12.5, 11.2)), Vertex("SVN", (09.7, 08.7)), Vertex("ESP", (02.8, 04.8)),
  Vertex("SWE", (18.6, 19.0)), Vertex("CHE", (06.6, 09.3)), Vertex("TUR", (15.5, 04.2)),
  Vertex("UKR", (14.2, 11.0)), Vertex("VAT", (05.4, 04.8)),
]

EDGES = [
  Edge("ALB", "XKX", 186),  Edge("ALB", "MKD", 153),  Edge("ALB", "GRC", 500), 
  Edge("ARM", "GEO", 172),  Edge("ARM", "TUR", 992),  Edge("ALB", "MNE", 131), 
  Edge("AND", "FRA", 709),  Edge("AND", "ESP", 493),  Edge("AUT", "DEU", 524), 
  Edge("AUT", "CZE", 251),  Edge("AUT", "SVK", 55),   Edge("AUT", "HUN", 214), 
  Edge("AUT", "SVN", 278),  Edge("AUT", "ITA", 764),  Edge("AUT", "CHE", 804), 
  Edge("AUT", "LIE", 526),  Edge("BLR", "RUS", 676),  Edge("BLR", "UKR", 434), 
  Edge("BLR", "POL", 475),  Edge("BLR", "LTU", 172),  Edge("BLR", "LVA", 405), 
  Edge("BEL", "NLD", 209),  Edge("BEL", "DEU", 657),  Edge("BEL", "LUX", 155), 
  Edge("BEL", "FRA", 238),  Edge("BIH", "HRV", 290),  Edge("BIH", "SRB", 195), 
  Edge("BIH", "MNE", 173),  Edge("BGR", "ROU", 295),  Edge("BGR", "SRB", 329), 
  Edge("BGR", "MKD", 174),  Edge("BGR", "GRC", 525),  Edge("BGR", "TUR", 853), 
  Edge("HRV", "SVN", 117),  Edge("HRV", "HUN", 299),  Edge("HRV", "SRB", 368), 
  Edge("HRV", "MNE", 458),  Edge("CZE", "DEU", 281),  Edge("CZE", "POL", 517), 
  Edge("CZE", "SVK", 289),  Edge("DEU", "DNK", 355),  Edge("EST", "RUS", 867), 
  Edge("EST", "LVA", 277),  Edge("FIN", "NOR", 787),  Edge("FIN", "RUS", 892), 
  Edge("FIN", "SWE", 396),  Edge("FRA", "LUX", 287),  Edge("DEU", "FRA", 877), 
  Edge("CHE", "FRA", 410),  Edge("FRA", "ITA", 1105), Edge("FRA", "MCO", 689), 
  Edge("ESP", "FRA", 1053), Edge("DEU", "NLD", 576),  Edge("DEU", "LUX", 602), 
  Edge("CHE", "DEU", 876),  Edge("DEU", "POL", 517),  Edge("GEO", "RUS", 1646), 
  Edge("GEO", "TUR", 1025), Edge("GRC", "MKD", 488),  Edge("GRC", "TUR", 818), 
  Edge("HUN", "SRB", 318),  Edge("HUN", "SVN", 381),  Edge("HUN", "ROU", 644), 
  Edge("HUN", "UKR", 899),  Edge("HUN", "SVK", 161),  Edge("CHE", "ITA", 697),
  Edge("ITA", "SVN", 489),  Edge("ITA", "SMR", 226),  Edge("ITA", "VAT", 4),
  Edge("MNE", "XKX", 158),  Edge("SRB", "XKX", 245),  Edge("MKD", "XKX", 77),
  Edge("LTU", "LVA", 264),  Edge("LVA", "RUS", 842),  Edge("CHE", "LIE", 278),
  Edge("LTU", "POL", 393),  Edge("LTU", "RUS", 790),  Edge("MDA", "ROU", 358),
  Edge("MDA", "UKR", 401),  Edge("MNE", "SRB", 282),  Edge("MKD", "SRB", 322),
  Edge("NOR", "SWE", 416),  Edge("NOR", "RUS", 1643), Edge("POL", "SVK", 532),
  Edge("POL", "UKR", 689),  Edge("POL", "RUS", 1151), Edge("ESP", "PRT", 502),
  Edge("ROU", "UKR", 747),  Edge("ROU", "SRB", 448),  Edge("RUS", "UKR", 756),
  Edge("SVK", "UKR", 1004), 
]

for edge in EDGES:
  MATRIX[edge.begin][edge.end] = True
  MATRIX[edge.end][edge.begin] = True

def construct_graph():
  graph = nx.Graph()
  for edge in EDGES:
    graph.add_edge(edge.begin, edge.end, weight = edge.weight)
  return graph
