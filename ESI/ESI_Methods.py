from ESI import ESI_Base

class Methods(ESI_Base.Base):

    esiURL = "https://esi.evetech.net/"

    def alliance_corporations(self, arguments):
            
        return self.makeRequest(
            endpoint = "/alliances/{alliance_id}/corporations/",
            url = (self.esiURL + "latest/alliances/" + str(arguments["alliance_id"]) + "/corporations/?datasource=tranquility"), 
            retries = (arguments["retries"] if "retries" in arguments else 0)
        )

    def character(self, arguments):
            
        return self.makeRequest(
            endpoint = "/characters/{character_id}/",
            url = (self.esiURL + "latest/characters/" + str(arguments["character_id"]) + "/?datasource=tranquility"), 
            retries = (arguments["retries"] if "retries" in arguments else 0)
        )

    def corporation(self, arguments):
            
        return self.makeRequest(
            endpoint = "/corporations/{corporation_id}/",
            url = (self.esiURL + "latest/corporations/" + str(arguments["corporation_id"]) + "/?datasource=tranquility"), 
            retries = (arguments["retries"] if "retries" in arguments else 0)
        )
    
    def contracts(self, arguments):
        
        page = (arguments["page"] if "page" in arguments else 1)
    
        return self.makeRequest(
            endpoint = "/contracts/public/{region_id}/",
            url = (self.esiURL + "latest/contracts/public/" + str(arguments["region_id"]) + "/?datasource=tranquility&page=" + str(page)), 
            retries = (arguments["retries"] if "retries" in arguments else 0)
        )

    def contract_items(self, arguments):
        
        page = (arguments["page"] if "page" in arguments else 1)
    
        return self.makeRequest(
            endpoint = "/contracts/public/items/{contract_id}/",
            url = (self.esiURL + "latest/contracts/public/items/" + str(arguments["contract_id"]) + "/?datasource=tranquility&page=" + str(page)), 
            retries = (arguments["retries"] if "retries" in arguments else 0)
        )

    def regions(self, arguments):
    
        return self.makeRequest(
            endpoint = "/universe/regions/{region_id}/",
            url = (self.esiURL + "latest/universe/regions/" + str(arguments["region_id"]) + "/?datasource=tranquility"), 
            retries = (arguments["retries"] if "retries" in arguments else 0)
        )

    def stations(self, arguments):
    
        return self.makeRequest(
            endpoint = "/universe/stations/{station_id}/",
            url = (self.esiURL + "latest/universe/stations/" + str(arguments["station_id"]) + "/?datasource=tranquility"), 
            retries = (arguments["retries"] if "retries" in arguments else 0)
        )

    def structures(self, arguments):
    
        return self.makeRequest(
            endpoint = "/universe/structures/{structure_id}/",
            url = (self.esiURL + "latest/universe/structures/" + str(arguments["structure_id"]) + "/?datasource=tranquility"), 
            accessToken = self.accessToken, 
            retries = (arguments["retries"] if "retries" in arguments else 0)
        )

