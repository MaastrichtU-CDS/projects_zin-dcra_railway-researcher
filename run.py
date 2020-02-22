from railway_researcher import RailwayResearcher
import json
import time

keycloakUrl = "https://dcra-keycloak.railway.medicaldataworks.nl"
keycloakClient = "johan"
keycloakToken = "b7940067-f9a7-41fb-b74b-f672fcdbfb6e"
railwayUrl = "https://dcra.railway.medicaldataworks.nl"

railway = RailwayResearcher(keycloakUrl, keycloakClient, keycloakToken, railwayUrl)
train = railway.createTrain("statistics", "registry.gitlab.com/um-cds/projects/zin-dcra/prototypetrain:master", "03838bb4-8103-4a98-a9c3-d4848b13b3f6", 2)
print("====================Train====================")
print(train)

task1 = railway.createTask(train, "REQUESTED", "", "maastro", 0, 0, False, "")
print("====================Task 1====================")
print(task1)

taskResult = railway.getTaskResult(task1, waitCompleted=True)
print("====================Result====================")
print(taskResult)