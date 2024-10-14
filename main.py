from flask import Flask, request, jsonify, render_template
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

graph = {
    'Delhi': {'Agra': 200, 'Jaipur': 260},
    'Agra': {'Delhi': 200, 'Kanpur': 270},
    'Jaipur': {'Delhi': 260, 'Udaipur': 400},
    'Kanpur': {'Agra': 270, 'Lucknow': 80},
    'Lucknow': {'Kanpur': 80, 'Varanasi': 300},
    # Add more cities and distances here...
}


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
    
    return jsonify({'distance': distance, 'path': formatted_path})

if __name__ == '__main__':
    app.run(debug=True)



