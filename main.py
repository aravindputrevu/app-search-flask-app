from flask import Flask, render_template, request     
from elastic_app_search import Client
import json

app = Flask(__name__)

with open("config.json") as json_data_file:
    config = json.load(json_data_file)

client = Client(
    base_endpoint=config['appsearch']['base_endpoint'],
    api_key=config['appsearch']['api_key'],
    use_https=True)

engine_name = config['appsearch']['engine_name']

@app.route("/")
def home():
    data = client.search(engine_name, "", {})
    return render_template("home.html" , data=data)

@app.route("/search", methods = ['POST'])
def search():
    if request.method == 'POST':
      query = request.form['search']
    data = client.search(engine_name, query, {})
    return render_template("results.html" , data=data)
     
@app.route("/index")
def index():
    # Opening JSON file 
    f = open('data.json',) 

    # returns JSON object as  
    # a dictionary 
    documents = json.load(f)
    data = client.index_documents(engine_name, documents)
    return render_template("about.html" , data=data)
    
if __name__ == "__main__":
    app.run(debug=False)