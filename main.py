from flask import Flask, render_template, request     
from elastic_enterprise_search import AppSearch
from elasticapm.contrib.flask import ElasticAPM
import json
import logging

app = Flask(__name__)

with open("config.json") as json_data_file:
    config = json.load(json_data_file)

apm = ElasticAPM(app,logging=logging.ERROR,
server_url=config['apm']['server_url'] ,
 service_name=config['apm']['service_name'], 
 secret_token=config['apm']['secret_token'])

client = AppSearch(
    config['appsearch']['base_endpoint'],
    http_auth=config['appsearch']['api_key'])

engine_name = config['appsearch']['engine_name']

@app.route("/")
def home():
    data = client.search(engine_name, body={
        "query": ""
    })
    return render_template("home.html" , data=data)

@app.route("/search", methods = ['POST'])
def search():
    if request.method == 'POST':
      query = request.form['search']
    data = client.search(engine_name, body={
        "query": query
    })
    return render_template("results.html" , data=data)
    
if __name__ == "__main__":
    app.run(debug=False)