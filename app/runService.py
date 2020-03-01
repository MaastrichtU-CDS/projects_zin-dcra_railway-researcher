from flask import Flask, Response, request, send_file, abort, render_template
import json
from railway_researcher import RailwayResearcher

# Create web application
app = Flask('ZIN DCRA Train Executor')

with open('config.json', 'r') as file:
    config = json.load(file)

######################################################################################
# Various webpage controller functions
######################################################################################
def getRailway():
    return RailwayResearcher(config['keycloakUrl'], config['keycloakClient'], config['keycloakToken'], config['railwayUrl'])

@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/', methods=["POST"])
def createRun():
    railway = getRailway()
    train = railway.createTrain("statistics", "registry.gitlab.com/um-cds/projects/zin-dcra/prototypetrain:master", "03838bb4-8103-4a98-a9c3-d4848b13b3f6", 2)
    inputData = {
        "query": """
            PREFIX db: <http://localhost/rdf/ontology/>
            PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT (IRI(concat("http://term.local/", ?genderString)) AS ?gender)
            WHERE {
                ?tt ?p db:Tumour_Treatment.
                ?tt dbo:has_column [
                    rdf:type db:Tumour_Treatment.Geslacht;
                    dbo:has_value ?genderString;
                ].
            }"""
    }
    railway.createTask(train, "REQUESTED", "", "maastro", 0, 0, False, json.dumps(inputData))
    railway.createTask(train, "REQUESTED", "", "maastro", 0, 0, True, "")
    return render_template("requested.html", trainId=train['id'])


@app.route('/train/<int:trainId>')
def checkRun(trainId):
    railway = getRailway()
    trainResult = railway.getTrainResult(trainId)

    if "latestTask" in trainResult:
        trainResult['latestTask']['result'] = json.loads(trainResult['latestTask']['result'])
        if len(trainResult['latestTask']['result']['categoricalStats']) > 0:
            trainResult['latestTask']['result']['categoricalStats'] = json.loads(trainResult['latestTask']['result']['categoricalStats'])
            print(trainResult['latestTask']['result']['categoricalStats'])
        if len(trainResult['latestTask']['result']['numericalStats']) > 0:
            trainResult['latestTask']['result']['numericalStats'] = json.loads(trainResult['latestTask']['result']['numericalStats'])
    
    return render_template("trainResult.html", trainResult=trainResult)


app.run(debug=True, host='0.0.0.0', port=80)