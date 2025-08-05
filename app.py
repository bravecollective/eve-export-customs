import inspect
import os
import json
import time

from datetime import datetime
from csv import DictWriter

import ESI
from Terminus import RelayTerminus

def dataFile(extraFolder):

    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.join(os.path.dirname(os.path.abspath(filename)))

    dataLocation = str(path) + extraFolder

    return(dataLocation)

class Contract:
    
    def __init__(self, id, type, issuer_id, issuer_corporation_id, for_corp, price, region_id, region_name, location_id):
        
        self.id = id
        self.type = type
        self.issuer_id = issuer_id
        self.issuer_name = None
        self.valid_issuer_token = True
        self.for_corp = for_corp
        self.issuer_corporation_id = issuer_corporation_id
        self.issuer_corporation_name = None
        self.price = price
        self.location_id = location_id
        self.location_name = None
        self.location_type_id = None
        self.location_type_name = None
        self.location_accessible = True
        self.system_id = None
        self.system_name = None
        self.region_id = region_id
        self.region_name = region_name
        self.unique_items = {}
                
    def get_issuer_data(self):
        
        esi_handler = ESI.Handler()

        issuer_corp_request = esi_handler.call("/corporations/{corporation_id}/", corporation_id=self.issuer_corporation_id, retries=2)

        if issuer_corp_request["Success"]:
            
            self.issuer_corporation_name = issuer_corp_request["Data"]["name"]
            
        else:
            
            raise Exception(
                "ISSUER CORP ERROR\n\nRepsonse Data: {data}\n\nResponse Headers: {headers}".format(
                    data=issuer_corp_request["Data"],
                    headers=issuer_corp_request["Headers"]
                )
            )

        issuer_request = esi_handler.call("/characters/{character_id}/", character_id=self.issuer_id, retries=2)

        if issuer_request["Success"]:
            
            self.issuer_name = issuer_request["Data"]["name"]
            
        else:
            
            raise Exception(
                "ISSUER ERROR\n\nRepsonse Data: {data}\n\nResponse Headers: {headers}".format(
                    data=issuer_request["Data"],
                    headers=issuer_request["Headers"]
                )
            )
        
    def get_items(self, type_data):
        
        esi_handler = ESI.Handler()
        
        current_page = 1
        max_page = 1
        
        while (current_page <= max_page):
            items_request = esi_handler.call("/contracts/public/items/{contract_id}/", contract_id=self.id, page=current_page, retries=2)
            
            if items_request["Success"]:
                
                max_page = int(items_request["Headers"]["X-Pages"])
                
                for each_item in items_request["Data"]:

                    if each_item["is_included"]:

                        self.unique_items[each_item["type_id"]] = type_data[str(each_item["type_id"])]
                
            else:
                
                raise Exception(
                    "ITEMS ERROR\n\nRepsonse Data: {data}\n\nResponse Headers: {headers}".format(
                        data=items_request["Data"],
                        headers=items_request["Headers"]
                    )
                )
            
            current_page += 1
    
    def get_location(self, auth_handler, login_name, type_data, geographic_information):

        if 60000000 <= self.location_id <= 64000000:

            esi_handler = ESI.Handler()

            location_request = esi_handler.call("/universe/stations/{station_id}/", station_id=self.location_id, retries=2)

            if location_request["Success"]:

                self.location_name = location_request["Data"]["name"]
                self.location_type_id = location_request["Data"]["type_id"]
                self.location_type_name = type_data[str(self.location_type_id)]
                self.system_id = location_request["Data"]["system_id"]
                self.system_name = geographic_information[str(self.system_id)]["name"]

            else:

                raise Exception(
                    "STATIONS ERROR\n\nRepsonse Data: {data}\n\nResponse Headers: {headers}".format(
                        data=location_request["Data"],
                        headers=location_request["Headers"]
                    )
                )

        else:

            access_token = auth_handler.getAccessToken(self.issuer_id, login_name)
                    
            if access_token is None:

                self.valid_issuer_token = False
                return
        
            esi_handler = ESI.Handler(access_token)

            location_request = esi_handler.call("/universe/structures/{structure_id}/", structure_id=self.location_id, retries=2)
        
            if location_request["Success"]:

                self.location_name = location_request["Data"]["name"]
                self.location_type_id = location_request["Data"]["type_id"]
                self.location_type_name = type_data[str(self.location_type_id)]
                self.system_id = location_request["Data"]["solar_system_id"]
                self.system_name = geographic_information[str(self.system_id)]["name"]

            else:

                self.location_accessible = False

class App:
    
    def __init__(self, target_alliances, target_corporations, target_exclusions, target_regions, core_info):
        
        self.target_corporations = target_corporations
        self.target_alliances = target_alliances
        self.target_exclusions = target_exclusions
        self.target_regions = target_regions
        self.corporations = target_corporations
        
        self.auth_handler = ESI.NeucoreAuth(core_info["AppID"], core_info["AppSecret"], core_info["AppURL"])
        self.core_info = core_info
        self.esi_handler = ESI.Handler()
        
        self.contracts = {}
        
        self.pull_static()
        self.build_targets()
        self.get_contracts()
        
    def pull_static(self):
        
        with open(dataFile("/static") + "/TypeIDs.json") as knownData:
            self.type_ids = json.load(knownData)
            
        with open(dataFile("/static") + "/geographicInformationV3.json") as knownData:
            self.geographic_data = json.load(knownData)
            
    def build_targets(self):
        
        for each_alliance in self.target_alliances:
            
            corporations_request = self.esi_handler.call("/alliances/{alliance_id}/corporations/", alliance_id=each_alliance, retries=2)
            
            if corporations_request["Success"]:
                self.corporations += corporations_request["Data"]
                
            else:
                raise Exception(
                    "CORPORATIONS ERROR\n\nRepsonse Data: {data}\n\nResponse Headers: {headers}".format(
                        data=corporations_request["Data"],
                        headers=corporations_request["Headers"]
                    )
                )
                
        self.corporations = [int(ids) for ids in self.corporations if str(ids) not in self.target_exclusions]
        
    def get_contracts(self):

        for each_region in self.target_regions:
            
            regions_request = self.esi_handler.call("/universe/regions/{region_id}/", region_id=each_region, retries=2)
            
            if regions_request["Success"]:
                region_name = regions_request["Data"]["name"]
                
            else:
                raise Exception(
                    "REGIONS ERROR\n\nRepsonse Data: {data}\n\nResponse Headers: {headers}".format(
                        data=regions_request["Data"],
                        headers=regions_request["Headers"]
                    )
                )

            current_page = 1
            max_page = 1

            while (current_page <= max_page):

                contracts_request = self.esi_handler.call("/contracts/public/{region_id}/", region_id=each_region, page=current_page, retries=2)
                
                if contracts_request["Success"]:

                    for each_contract in contracts_request["Data"]:

                        print("Checking {region} contract {contract_id}...".format(region=region_name, contract_id=each_contract["contract_id"]))

                        if each_contract["issuer_corporation_id"] in self.corporations:

                            print("{contract_id} in target corporation {corporation_id}. Processing...".format(contract_id=each_contract["contract_id"], corporation_id=each_contract["issuer_corporation_id"]))

                            self.contracts[each_contract["contract_id"]] = Contract(
                                id = each_contract["contract_id"], 
                                type = each_contract["type"], 
                                issuer_id = each_contract["issuer_id"], 
                                issuer_corporation_id = each_contract["issuer_corporation_id"], 
                                for_corp = "for_corporation" in each_contract and each_contract["for_corporation"], 
                                price = each_contract["price"], 
                                region_id = each_region, 
                                region_name = region_name, 
                                location_id = each_contract["start_location_id"]
                            )

                            self.contracts[each_contract["contract_id"]].get_issuer_data()
                            self.contracts[each_contract["contract_id"]].get_items(self.type_ids)
                            self.contracts[each_contract["contract_id"]].get_location(self.auth_handler, self.core_info["LoginName"], self.type_ids, self.geographic_data)
                    
                else:
                    raise Exception(
                        "CONTRACTS ERROR\n\nRepsonse Data: {data}\n\nResponse Headers: {headers}".format(
                            data=contracts_request["Data"],
                            headers=contracts_request["Headers"]
                        )
                    )
                
                current_page += 1

    def generate_report(self, title, target_types, platform, url):

        report_template = "*Contract Found in [{region}] {structure} ({structure_type})*\n*Issuer:* {issuer} ({corporation})\n{warnings}\n*Contraband Items:*\n```\n{items}\n```"

        report_components = []

        report_components.append(f"*----- BEGIN {title} -----*\n\n")

        for each_contract_id, each_contract in self.contracts.items():

            overlap = [x for x in each_contract.unique_items.values() if x in target_types]

            if overlap:

                warnings = []
                if not each_contract.valid_issuer_token:
                    warnings.append("*WARNING: Character does not have a valid Neucore token.*")
                if not each_contract.location_accessible:
                    warnings.append("*WARNING: Character cannot access the contract location.*")

                report_components.append(report_template.format(
                    region=each_contract.region_name,
                    structure=each_contract.location_name,
                    structure_type=each_contract.location_type_name,
                    issuer=each_contract.issuer_name,
                    corporation=each_contract.issuer_corporation_name,
                    warnings="\n".join(warnings),
                    items="\n".join(overlap)
                ))

        report_components.append(f"*----- END {title} -----*\n\n")

        for each_message in report_components:
            relay = RelayTerminus(each_message, platform, url)
            relay.send(5)
