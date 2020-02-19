class RailwayResearcher:
    requests = __import__('requests')
    json = __import__("json")
    def __init__(self, url, user, password):
        self.apiUrl = url
        self.apiUser = user
        self.apiPass = password
        self.apiToken = None
        self.__connect()
    
    def __connect(self):
        response = self.requests.post(self.apiUrl + "/auth/realms/railway/protocol/openid-connect/token",
            data={"grant_type": "client_credentials"},
            auth=(self.apiUser, self.apiPass))
        self.apiToken = self.json.loads(response.text)['access_token']