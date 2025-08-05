import inspect
import os
import configparser
import argparse

from pathlib import Path

import app

#If you've moved your config.ini file, set this variable to the path of the folder containing it (no trailing slash).
CONFIG_PATH_OVERRIDE = None

def dataFile(extraFolder):

    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.join(os.path.dirname(os.path.abspath(filename)))

    dataLocation = str(path) + extraFolder

    return(dataLocation)

configPath = (CONFIG_PATH_OVERRIDE) if (CONFIG_PATH_OVERRIDE is not None) else (dataFile("/config"))

if Path(configPath + "/config.ini").is_file():

    config = configparser.ConfigParser()
    config.read(dataFile("/config") + "/config.ini")

    targetAlliances = str(config["App"]["TargetAlliances"]).replace(", ", ",").split(",")
    targetCorps = str(config["App"]["TargetCorps"]).replace(", ", ",").split(",")
    targetExclusions = str(config["App"]["TargetExclusions"]).replace(", ", ",").split(",")
    targetRegions = str(config["App"]["TargetRegions"]).replace(", ", ",").split(",")
    targetTypes = str(config["App"]["TargetTypes"]).replace(", ", ",").split(",")
    reportTitle = config["App"]["ReportTitle"]
    webhookPlatform = config["App"]["WebhookPlatform"]
    webhookURL = config["App"]["WebhookURL"]
    coreInfo = config["NeuCore Authentication"]

else:

    try:

        targetAlliances = str(os.environ["ENV_CONTRACT_MONITORING_TARGET_ALLIANCES"]).replace(", ", ",").split(",")
        targetCorps = str(os.environ["ENV_CONTRACT_MONITORING_TARGET_CORPS"]).replace(", ", ",").split(",")
        targetExclusions = str(os.environ["ENV_CONTRACT_MONITORING_TARGET_EXCLUSIONS"]).replace(", ", ",").split(",")
        targetRegions = str(os.environ["ENV_CONTRACT_MONITORING_TARGET_REGIONS"]).replace(", ", ",").split(",")
        targetTypes = str(os.environ["ENV_CONTRACT_MONITORING_TARGET_TYPES"]).replace(", ", ",").split(",")
        reportTitle = os.environ["ENV_CONTRACT_MONITORING_REPORT_TITLE"] if "ENV_CONTRACT_MONITORING_REPORT_TITLE" in os.environ else None
        webhookPlatform = os.environ["ENV_CONTRACT_MONITORING_WEBHOOK_PLATFORM"] if "ENV_CONTRACT_MONITORING_WEBHOOK_PLATFORM" in os.environ else None
        webhookURL = os.environ["ENV_CONTRACT_MONITORING_WEBHOOK_URL"] if "ENV_CONTRACT_MONITORING_WEBHOOK_URL" in os.environ else None
        coreInfo = {
            "AppID": os.environ["ENV_CONTRACT_MONITORING_NEUCORE_APP_ID"], 
            "AppSecret": os.environ["ENV_CONTRACT_MONITORING_NEUCORE_APP_SECRET"], 
            "AppURL": os.environ["ENV_CONTRACT_MONITORING_NEUCORE_APP_URL"],
            "LoginName": os.environ["ENV_CONTRACT_MONITORING_NEUCORE_LOGIN_NAME"]
        }

    except:

        raise Warning("No Configuration File or Required Environment Variables Found!")

#Cleanup of possible parsing issues
if "" in targetAlliances:
    targetAlliances.remove("")
if "" in targetCorps:
    targetCorps.remove("")
if "" in targetExclusions:
    targetExclusions.remove("")

processor = app.App(targetAlliances, targetCorps, targetExclusions, targetRegions, coreInfo)
processor.generate_report(reportTitle, targetTypes, webhookPlatform, webhookURL)
