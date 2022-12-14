from app.railway_researcher import RailwayResearcher
import json
import time
import html

keycloakUrl = "https://dcra-keycloak.railway.medicaldataworks.nl"
keycloakClient = "ananya"
keycloakToken = "c3b77319-0ee5-444a-8391-615c1d037ed9"
railwayUrl = "https://dcra.railway.medicaldataworks.nl"

railway = RailwayResearcher(keycloakUrl, keycloakClient, keycloakToken, railwayUrl)

train = railway.createTrain("statistics", "registry.gitlab.com/um-cds/projects/zin-dcra/prototypetrain:master", "03838bb4-8103-4a98-a9c3-d4848b13b3f6", 2)
print("====================Train====================")
print(train)

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

task1 = railway.createTask(train, "REQUESTED", "", "maastro", 0, 0, False, json.dumps(inputData))
print("====================Task 1====================")
print(task1)

masterTask = railway.createTask(train, "REQUESTED", "", "maastro", 0, 0, True, "")
print("====================MasterTask================")
print(masterTask)

taskResult = railway.getTaskResult(masterTask, waitCompleted=False)
print("====================MasterResult====================")
print(taskResult)

trainResult = railway.getTrainResult(train['id'], waitCompleted=True)
print("====================TrainResult====================")
print(trainResult)