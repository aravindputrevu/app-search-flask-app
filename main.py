import json

from elasticsearch import Elasticsearch, helpers, ElasticsearchException
from elasticsearch_dsl import Search
from flask import Flask, render_template, request

app = Flask(__name__)

with open("config.json") as json_data_file:
    config = json.load(json_data_file)

es = Elasticsearch(
    cloud_id=config['elasticsearch']['cloud_id'],
    api_key=(config['elasticsearch']['api_key'], config['elasticsearch']['api_key_secret'])
)


@app.route("/index")
def index():
    # Opening JSON file
    f = open('movies.json', )
    documents = []
    for i in f.readlines():
        documents.append(i)

    # use bulk helper
    data = helpers.bulk(
        es,
        documents,
        index="movies",
    )
    return render_template("about.html", data=data)


@app.route("/search", methods=['POST'])
def search_es():
    if request.method == 'POST':
        query = request.form['search']
    data = es.search(index="movies", body={"query": {
        "multi_match": {
            "query": query,
            "fields": ["title", "plot"]
        }
    }})
    movies_list = []
    for i in data['hits']['hits']:
        movies_list.append(i['_source'])
    return render_template("index.html", data=movies_list)


@app.route("/search-dsl", methods=['GET'])
def search_dsl():
    # if request.method == 'POST':
    #    query = request.form['search']
    q = Search(using=es, index="movies").query("match", title="robert")
    res = q.execute()
    movies_list = []
    if res:
        for hit in res:
            movies_list.append(hit)
    return render_template("index.html", data=movies_list)


@app.route("/")
def home():
    data = ""
    es_error = ""
    try:
        data = es.search(index="movies", body={"query": {"match_all": {}}})
    except ElasticsearchException as e:
        es_error = "Configure cluster credentials in \"config.json\" and Index data with by calling \"/index\" endpoint"
        print(es_error)
    movies_list = []
    if data:
        for i in data['hits']['hits']:
            movies_list.append(i['_source'])
    return render_template("index.html", data=movies_list, es_error=es_error)


if __name__ == "__main__":
    app.run(debug=False)
