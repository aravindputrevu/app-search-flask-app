import json

from elastic_enterprise_search import AppSearch
from flask import Flask, render_template, request

app = Flask(__name__)

with open("config.json") as json_data_file:
    config = json.load(json_data_file)

client = AppSearch(
    config['appsearch']['base_endpoint'],
    http_auth=config['appsearch']['api_key'])

engine_name = config['appsearch']['engine_name']


@app.route("/")
def home():
    data = client.search(engine_name, body={
        "query": ""
    })
    return render_template("index.html", data=data)


@app.route("/search", methods=['POST'])
def search():
    if request.method == 'POST':
        query = request.form['search']
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
    app.run(debug=False)
