from ESI import ESI_Methods

class MethodRegister(ESI_Methods.Methods):

    def initalizeMethodList(self):
    
        self.methodList = {}
        
        self.register(
            endpoint = "/alliances/{alliance_id}/corporations/", 
            method = "alliance_corporations",
            requiredArguments = ["alliance_id"]
        )
        
        self.register(
            endpoint = "/characters/{character_id}/", 
            method = "character",
            requiredArguments = ["character_id"]
        )

        self.register(
            endpoint = "/corporations/{corporation_id}/", 
            method = "corporation",
            requiredArguments = ["corporation_id"]
        )

        self.register(
            endpoint = "/contracts/public/{region_id}/", 
            method = "contracts",
            requiredArguments = ["region_id"]
        )

        self.register(
            endpoint = "/contracts/public/items/{contract_id}/", 
            method = "contract_items",
            requiredArguments = ["contract_id"]
        )

        self.register(
            endpoint = "/universe/names/", 
            method = "names",
            requiredArguments = ["items"]
        )

        self.register(
            endpoint = "/universe/regions/{region_id}/", 
            method = "regions",
            requiredArguments = ["region_id"]
        )

        self.register(
            endpoint = "/universe/stations/{station_id}/", 
            method = "stations",
            requiredArguments = ["station_id"]
        )

        self.register(
            endpoint = "/universe/structures/{structure_id}/", 
            method = "structures",
            requiredArguments = ["structure_id"]
        )
    
        self.register(
            endpoint = "/universe/types/", 
            method = "types",
            requiredArguments = []
        )

    def register(self, endpoint, method, requiredArguments):
    
        self.methodList[endpoint] = {"Name": method, "Required Arguments": requiredArguments}
    