import json

#store jsonfile into data
with open('generatedGraph.json') as json_file:
  data = json.load(json_file)

#define vertices, edges
vertices = data['nodes']
edges = data['edges']
#initialization of the edges and the graph that is used as input for the main algorithm
edge_list = []
graph_input = {}


#function that puts every edge into a 3-tuple and puts them into a list
def set_edges(edges, edge_list):
  for edge in edges:
    edge_list.append((edge['source'],edge['target'],edge['cost']))

#function call gives a list of 3-tuples: [(node,neighbor,cost)]
set_edges(edges, edge_list)


#function that sets all existent neighbors of every node
def set_neighbors(edge_list):
  for edge in edge_list:
    if edge[0] not in graph_input:
      graph_input[edge[0]] = {edge[1]:edge[2]} 
    if edge[1] not in graph_input:
      graph_input[edge[1]] = {edge[0]:edge[2]}
    else:
      graph_input[edge[0]].update({edge[1]:edge[2]})
      graph_input[edge[1]].update({edge[0]:edge[2]})

set_neighbors(edge_list)


#[(node_i , i)] list of tuples
vertices_keys = []
length = len(vertices)
for i in range(0,length):
  label = vertices[i]['label']
  vertices_keys.append((label, i))

#convert index to node
def inttonode(index):
  convert = vertices_keys[index]
  if index == convert[1]:
    return convert[0]

#convert node to int
def nodetoint(node):
  for keys in vertices_keys:
    if keys[0] == node: 
      convert = keys[1]
  return convert

#initialize start, end
start = nodetoint(vertices[18]['label'])
end = nodetoint(vertices[246]['label'])

#main algorithm (dijkstra)
def dijkstra(graph,start,end,visited=[],distances={},predecessors={}):
#termination condition / base case
  if start == end:
    #save shortest path from start to end
    path=[]
    pred=end
    while pred != None:
      path.append(inttonode(pred))
      pred=predecessors.get(pred,None)
    #print shortest path
    path.reverse()
    print('shortest path: '+str(path)+" and it costs : "+str(distances[end])) 
  else:     
    #initialization for first walkthrough
    if not visited: 
      distances[start]=0
    #visit the neighbors
    for neighbor in graph[start] :
      if neighbor not in visited:
        new_distance = distances[start] + graph[start][neighbor]
        if new_distance < distances.get(neighbor,float('inf')):
          distances[neighbor] = new_distance
          predecessors[neighbor] = start
    #keep track of visited neighbors
    visited.append(start)
    #run dijkstra recursively with unseen neighbor x with lowest cost 
    unvisited={}
    for k in graph:
      if k not in visited:
        unvisited[k] = distances.get(k,float('inf'))        
    x=min(unvisited, key=unvisited.get)
    dijkstra(graph,x,end,visited,distances,predecessors)

dijkstra(graph_input, start, end)