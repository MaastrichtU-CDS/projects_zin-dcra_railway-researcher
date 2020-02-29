from railway_researcher import RailwayResearcher
import json
import time
import html

keycloakUrl = "https://dcra-keycloak.railway.medicaldataworks.nl"
keycloakClient = "johan"
keycloakToken = "b7940067-f9a7-41fb-b74b-f672fcdbfb6e"
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

taskResult = railway.getTaskResult(masterTask, waitCompleted=True)
print("====================Result====================")
print(taskResult)

# TODO: Add closing task
