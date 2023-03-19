class LaTeX:

  def __init__(self, output_path):
    self._file = None
    self._path = output_path + ".txt"
    self._colors = [
      "green!60", "cyan!60", "orange!60", "pink!60",
      "red", "magenta!60", "teal", "black", "violet!80"
    ]
  
  def __enter__(self):
    self._file = open(self._path, "w", encoding="utf8")
    return self
  
  def __exit__(self, exception_type, exception_value, traceback):
    self._file.close()
  
  def _write(self, line):
    self.write_raw("\\" + line)
  
  def _math(self, line):
    self.write_raw(f"${line}$")

  def basic_metrics(self, metrics):
    self._math("\\card{V} = " + str(metrics["vertices_count"]))
    self._math("\\card{E} = " + str(metrics["edges_count"]))

    self._math("\\minDegree{\MyGraph} = " + str(metrics["min_degree"]))
    self._math("\\maxDegree{\MyGraph} = " + str(metrics["max_degree"]))

    self._math("\\graphRadius{\MyGraph} = " + str(metrics["radius"]))
    self._math("\\graphDiameter{\MyGraph} = " + str(metrics["diameter"]))
    self._math("\\graphGirth{\MyGraph} = " + str(metrics["girth"]))

    self._math("\\graphCenter{\MyGraph} = \{" + ", ".join(metrics["center"]) + "\}")

    self._math("\\vertexConnectivity{\MyGraph} = " + str(metrics["vertex_connectivity"]))
    self._math("\\edgeConnectivity{\MyGraph} = " + str(metrics["edge_connectivity"]))
  
  def graph(self, vertices, edges):
    self._write("""begin{tikzpicture}[
      trim left = 1cm,
      every node/.style = {
        circle,
        inner sep = 2pt,
        outer sep = 0pt,
        draw = blue!80,
        line width = 0.5mm
      },
      every path/.style = {
        draw = blue!80,
        line width = 0.5mm
      }
    ]""")
    # borders
    self._write("draw[draw=red!50, thick] (0, 1.5) rectangle (20, 20);")

    for vertex in vertices:
      self._write(
        f"node[{self._get_options(vertex.options)}]" \
        f" ({vertex.name})" \
        f" at {vertex.position}" \
        f" {{{vertex.name}}};"
      )
    for edge in edges:
      self._write(
        f"draw[{self._get_options(edge.options)}]" \
        f" ({edge.begin}) -- ({edge.end}){self._get_weight(edge)};"
      )

    self._write("end{tikzpicture}")
  
  def write_raw(self, line):
    self._file.write(str(line) + "\n")

  def _get_options(self, options):
    result = []

    if options.get("vertex_color", None) is not None:
      color = options["vertex_color"]
      result.append(f"fill={self._colors[color]}")

    if options.get("edge_color", None) is not None:
      color = options["edge_color"]
      result.append(f"draw={self._colors[color]}")
      result.append(f"line width=3pt")

    if options.get("choose_vertex", None) is not None:
      if options.get("choose_vertex"):
        result.append(f"fill=blue!20")
      else:
        result.append(f"opacity=0.2")
      
    if options.get("choose_edge", None) is not None:
      if options.get("choose_edge"):
        result.append(f"draw=blue,line width=0.7mm")
      else:
        result.append(f"opacity=0.2")
    
    if options.get("arrow", None) is not None:
      result.append(f"->")

    return ",".join(result)

  def _get_weight(self, edge):
    if edge.options.get("draw_weight"):
      return f" node [label] {{{edge.weight}}}"
    return ""
