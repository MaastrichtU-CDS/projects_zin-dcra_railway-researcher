from datetime import datetime
import json
import requests
import time

class RailwayResearcher:
    def __init__(self, url, user, password, urlRailway):
        self.apiUrl = url
        self.apiUser = user
        self.apiPass = password
        self.apiToken = None
        self.railwayApi = urlRailway
        self.__connect()
    
    def __connect(self):
        response = requests.post(self.apiUrl + "/auth/realms/railway/protocol/openid-connect/token",
            data={"grant_type": "client_credentials"},
            auth=(self.apiUser, self.apiPass))
        self.apiToken = json.loads(response.text)['access_token']
    
    def createTrain(self, name, dockerImageUrl, ownerId):
        response = requests.post(self.railwayApi + "/api/trains?access_token=" + self.apiToken,
            json={
                "name": name,
                "dockerImageUrl": dockerImageUrl,
                "ownerId": ownerId,
                "calculationStatus":"REQUESTED", 
                "currentIteration":0
            },
            headers={
                "Content-Type": "application/json",
            })
        return response.json()
    
    def createTask(self, trainStruct, calculationStatus, result, stationId, iteration, currentIteration, master, input):
        response = requests.post(self.railwayApi + "/api/trains/"+str(trainStruct['id'])+"/tasks?access_token=" + self.apiToken,
            json={
                "creationTimestamp": datetime.now().isoformat(),
                "calculationStatus": calculationStatus,
                "result": result,
                "stationId": stationId,
                "iteration": iteration,
                "currentIteration": currentIteration,
                "master": master,
                "input": input
            },
            headers={
                "Content-Type": "application/json",
            })
        return response.json()
    
    def getTaskResult(self, taskStruct, waitCompleted=False):
        url = self.railwayApi + "/api/tasks/" + str(taskStruct['id']) + "?access_token=" + self.apiToken
        
        responseJson = requests.get(url).json()
        
        while (responseJson["calculationStatus"] in ["REQUESTED", "PROCESSING"]):
            time.sleep(5)
            responseJson = requests.get(url).json()
        
        return responseJson