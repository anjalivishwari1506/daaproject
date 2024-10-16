from flask import Flask, request, jsonify, render_template
import json
from graph import graph # importdistance data from different file

app = Flask(__name__)



def dijkstra(graph, start, end):
    import heapq
    queue = [(0, start, [])]
    seen = set()
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in seen:
            continue
        path = path + [node]
        if node == end:
            return (cost, path)
        seen.add(node)
        for next_node, distance in graph.get(node, {}).items():
            heapq.heappush(queue, (cost + distance, next_node, path))
    return (float('inf'), [])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/find-route', methods=['POST'])
def find_route():
    data = request.json
    source = data.get('source')
    destination = data.get('destination')
    
    if source not in graph or destination not in graph:
        return jsonify({'error': 'Invalid source or destination city'}), 400

    distance, path = dijkstra(graph, source, destination)
    
    if distance == float('inf'):
        return jsonify({'error': 'No route found'}), 404
    
    formatted_path = ' -> '.join(path)
    

    d = str(distance)+" Km" + "\n\n" 
    return jsonify({'distance': d , 'path': formatted_path})


if __name__ == '__main__':
    app.run(debug=True)
