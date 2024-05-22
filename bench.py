"""
Basic graph benchmarking
"""
import time
import networkx as nx
import rustworkx as rx
import networkit as nk
import igraph

def timed(func):
    """
    Function decorator to measure time
    """
    def inner_func(*args,**kwargs):
        start_time = time.perf_counter()
        func(*args,**kwargs)
        end_time = time.perf_counter()
        print(end_time-start_time)
    return inner_func

@timed
def nx_shortest_path(file_path, in_node_label, out_node_label):
    """
    Use NetworkX
    """
    di_graph: nx.DiGraph = nx.read_edgelist(file_path,create_using=nx.DiGraph())
    path = nx.astar_path(di_graph,in_node_label,out_node_label,lambda x,y:0)
    print(path)

@timed
def rx_shortest_path(file_path, in_node_label, out_node_label):
    """
    Use RustworkX
    """
    di_graph = rx.PyDiGraph().read_edge_list(file_path,labels=True)
    path = rx.astar_shortest_path(di_graph,di_graph.nodes().index(in_node_label),lambda x: x==out_node_label,lambda x: 1.,lambda x: 0.)
    print(list(map(di_graph.get_node_data,path)))

@timed
def nk_shortest_path(file_path, in_node_label, out_node_label):
    """
    Use NetworkIt
    """
    edge_list_reader = nk.graphio.EdgeListReader(separator="\t",firstNode=0,continuous=False,directed=True)
    di_graph = edge_list_reader.read(file_path)
    node_index_map = edge_list_reader.getNodeMap()
    index_node_map = {value:key for key,value in node_index_map.items()}
    path = nk.distance.AStar(di_graph, [0 for _ in range(di_graph.upperNodeIdBound())],node_index_map[in_node_label], node_index_map[out_node_label],True).run().getPath()
    print([in_node_label]+list(map(index_node_map.get,path))+[out_node_label])

@timed
def ig_shortest_path(file_path, in_node_label, out_node_label):
    """
    Use IGraph
    """
    di_graph = igraph.Graph(directed=True).Read(file_path, format="edges")
    di_graph.vs["name"] = list(map(str,range(0,len(di_graph.vs))))
    path = di_graph.get_shortest_path_astar(di_graph.vs["name"].index(in_node_label),di_graph.vs["name"].index(out_node_label),lambda graph,u,v:0)
    print([di_graph.vs[x]["name"] for x in path])

def main():
    """
    Controller function
    """
    file_path = "data/amazon.txt"
    in_node_label = "100"
    out_node_label = "150"
    nx_shortest_path(file_path, in_node_label, out_node_label)
    rx_shortest_path(file_path, in_node_label, out_node_label)
    nk_shortest_path(file_path, in_node_label, out_node_label)
    ig_shortest_path(file_path, in_node_label, out_node_label)

if __name__ == "__main__":
    """
    Entry point
    """
    main()