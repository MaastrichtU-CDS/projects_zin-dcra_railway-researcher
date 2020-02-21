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
        self.stations = [ ]
        self.__connect()
        self.__getStations()
    
    def __connect(self):
        response = requests.post(self.apiUrl + "/auth/realms/railway/protocol/openid-connect/token",
            data={"grant_type": "client_credentials"},
            auth=(self.apiUser, self.apiPass))
        self.apiToken = json.loads(response.text)['access_token']
    
    def __getStations(self):
        self.stations = requests.get(self.railwayApi + "/api/stations?access_token=" + self.apiToken).json()
    
    def __getStationIdByName(self, stationName):
        for station in self.stations:
            if station['name']==stationName:
                return station['id']
        return None
    
    def __checkValidStationId(self, stationId):
        for station in self.stations:
            if station['id'] == stationId:
                return True
        return False
    
    def createTrain(self, name, dockerImageUrl, ownerId, clientTaskCount):
        if len(self.stations)==0:
            print("No stations available")
            return None

        response = requests.post(self.railwayApi + "/api/trains?access_token=" + self.apiToken,
            json={
                "name": name,
                "dockerImageUrl": dockerImageUrl,
                "ownerId": ownerId,
                "calculationStatus":"REQUESTED", 
                "currentIteration":0,
                "clientTaskCount": clientTaskCount
            },
            headers={
                "Content-Type": "application/json",
            })
        return response.json()
    
    def createTask(self, trainStruct, calculationStatus, result, stationId, iteration, currentIteration, master, input):
        if type(stationId) == str:
            stationId = self.__getStationIdByName(stationId)
        
        if not self.__checkValidStationId(stationId):
            print("Could not create task. No valid station name or ID")
            return None

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