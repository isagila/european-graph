import shutil

from data import *
from latex import *
from solvers import *

if __name__ == "__main__":
  # Note: package postman_problems don't work with latests
  # versions of python. Python 3.7 works for me

  # Note: calculations can be a little long (1-2 minutes)

  output_dir = "output"
  if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
  os.mkdir(output_dir)
  os.chdir(output_dir)

  # -- calculate basic metrics for G -- #

  with LaTeX("basic_metrics") as latex:
    latex.basic_metrics(calculate_basic_metrics())

  # -- calculation for G with z3 -- #

  with LaTeX("minimum_vertex_coloring") as latex:
    latex.graph(*minimum_vertex_coloring())
  with LaTeX("minimum_edge_coloring") as latex:
    latex.graph(*minimum_edge_coloring())
  with LaTeX("maximum_clique") as latex:
    latex.graph(*maximum_clique())
  with LaTeX("maximum_independent_set") as latex:
    latex.graph(*maximum_independent_set())
  with LaTeX("maximum_matching") as latex:
    latex.graph(*maximum_matching())
  with LaTeX("minimum_vertex_cover") as latex:
    latex.graph(*minimum_vertex_cover())
  with LaTeX("minimum_edge_cover") as latex:
    latex.graph(*minimum_edge_cover())
  with LaTeX("minimum_edge_walk") as latex:
    latex.write_raw(minimum_edge_walk())

  # too slow, don't use
  # with LaTeX("minimum_vertex_walk") as latex:
  #   latex.write_raw(minimum_vertex_walk()) 

  # -- MST metrics G with networkx -- #

  mst = nx.minimum_spanning_tree(construct_graph())
  with LaTeX("minimum_spanning_tree") as latex:
    latex.graph(*minimum_spanning_tree(mst.edges))
  with LaTeX("centroid") as latex:
    latex.write_raw(centroid(mst.edges))
  with LaTeX("prufer_code") as latex:
    latex.write_raw(prufer_encode(mst))

  print("Done\n")
