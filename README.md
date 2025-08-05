# Eve Export Customs

Eve Export Customs is an application that checks public contracts belonging to certain alliances in certain regions for contraband items, designed for use with [neucore](https://github.com/tkhamez/neucore). 

## Requirements

* Python ≥ 3.13
  * [requests](https://pypi.org/project/requests/)
* A Neucore App
  * The `app-esi-token` role
  * An EVE Login with the following scopes:
    * `esi-universe.read_structures.v1`
    
## Setup
* Rename the Configuration File in `/config/config.ini.dist` to `/config/config.ini` and setup as needed. 
  * Alternatively, use the Environment Variables mentioned in the file.
