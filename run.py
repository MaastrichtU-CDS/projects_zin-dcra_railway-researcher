from railway_researcher import RailwayResearcher
import json
import time

keycloakUrl = "https://dcra-keycloak.railway.medicaldataworks.nl"
keycloakClient = "johan"
keycloakToken = "c9a295ff-bdde-47de-b82c-88ae5e38736d"
railwayUrl = "https://dcra.railway.medicaldataworks.nl"

railway = RailwayResearcher(keycloakUrl, keycloakClient, keycloakToken, railwayUrl)
train = railway.createTrain("statistics", "registry.gitlab.com/medicaldataworks/railway/prototypetrain:master", "03838bb4-8103-4a98-a9c3-d4848b13b3f6")
print("====================Train====================")
print(train)

task1 = railway.createTask(train, "COMPLETED", json.dumps({"calculation_result": 6}), "timh", 0, 0, False, "")
print("====================Task 1====================")
print(task1)

task2 = railway.createTask(train, "COMPLETED", json.dumps({"calculation_result": 10}), "johan", 0, 0, False, "")
print("====================Task 2====================")
print(task2)

task3 = railway.createTask(train, "REQUESTED", "", "johan", 0, 0, True, json.dumps({"iterations": 0}))
print("====================Task 3====================")
print(task3)

taskResult = railway.getTaskResult(task3, waitCompleted=True)
print("====================Result====================")
print(taskResult)