import json

from elastic_enterprise_search import AppSearch
from flask import Flask, render_template, request
from elasticapm.contrib.flask import ElasticAPM
import logging
import ecs_logging

app = Flask(__name__)

with open("config.json") as json_data_file:
    config = json.load(json_data_file)

client = AppSearch(
    config['appsearch']['base_endpoint'],
    http_auth=config['appsearch']['api_key'])

apm = ElasticAPM(app, logging=logging.INFO,
                 server_url=config['apm']['server_url'],
                 service_name=config['apm']['service_name'],
                 secret_token=config['apm']['secret_token'])

engine_name = config['appsearch']['engine_name']


@app.route("/")
def home():
    app.logger.info('Welcome to the Movies App!')
    data = client.search(engine_name, body={
        "query": ""
    })
    return render_template("index.html", data=data)


@app.route("/search", methods=['POST'])
def search():
    if request.method == 'POST':
        query = request.form['search']
        app.logger.info('Calling Search with query: %s', query)
    data = client.search(engine_name, body={
        "query": query
    })
    return render_template("index.html", data=data)


@app.route("/index")
def index():
    # Opening JSON file 
    f = open('data.json', )

    # returns JSON object as  
    # a dictionary 
    documents = json.load(f)
    data = client.index_documents(engine_name, documents)
    return render_template("about.html", data=data)


if __name__ == "__main__":
    handler = logging.StreamHandler()
    handler.setFormatter(ecs_logging.StdlibFormatter())
    app.logger.addHandler(handler)
    app.run(debug=False)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    handler = logging.StreamHandler()
    handler.setFormatter(ecs_logging.StdlibFormatter())
    app.logger.addHandler(handler)
    app.logger.setLevel(gunicorn_logger.level)
