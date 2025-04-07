from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

ES_URL = 'http://localhost:9200/logs/_search?pretty'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_logs():
    keyword = request.form.get('keyword', '')
    log_level = request.form.get('log_level', '')

    query = {
        'query': {
            'bool': {
                'must': [
                    {'match': {'message': keyword}}
                ]
            }
        }
    }
    if log_level:
        query['query']['bool']['must'].append({'match': {'message': log_level}})

    response = requests.post(ES_URL, json=query)
    if response.status_code == 200:
        results = response.json()['hits']['hits']
        logs = [{'message': hit['_source']['message']} for hit in results]
        return jsonify(logs)
    else:
        return jsonify({'error': 'Error retrieving logs'}), 500

@app.route('/recent')
def recent_logs():
    query = {
        'size': 10,
        'sort': [{'timestamp': {'order': 'desc'}}]
    }
    response = requests.post(ES_URL, json=query)
    if response.status_code == 200:
        results = response.json()['hits']['hits']
        logs = [{'message': hit['_source']['message']} for hit in results]
        return jsonify(logs)
    else:
        return jsonify({'error': 'Error retrieving recent logs'}), 500

if __name__ == '__main__':
    app.run(debug=True)