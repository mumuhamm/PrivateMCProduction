#!/usr/bin/env python3
import os

from python.utilityFunctions import *
#########################################
#########################################
CMSSW_BASE = os.environ.get("CMSSW_BASE")
genFragmentsDirectory = "Configuration/GenProduction/python/GenFragments/"
generator_fragments= [
                    "TSG-Run3Summer22EEGS-00025.py"
                    #"TSG-Run3Summer22EEGS-00030.py"
                    #"TSG-Run3Summer22EEGS-00029.py"
                    #"TSG-Run3Summer22EEGS-00024.py"
]


#Job steering parameters
era = "Run2022"
workAreaName = "tasks_BsToMuMuGamma_MCTunesRun3ECM13p6TeV"
eventsPerJob = 10
numberOfJobs = 4
outLFNDirBase = "/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/"
storage_element="T2_CH_CERN"
outputDatasetTag = "BsToMuMuGamma_14_1_0pre4_11_06_2024"
withPileUp = False
withReco = False
runLocal = True


#########################################
for aGenFragment in generator_fragments:

    requestName = aGenFragment.split("00025")[0].rstrip("-")
    requestName+="_"+era+"_"+outputDatasetTag
    process = runCMSDriver(era, withPileUp, withReco, genFragmentsDirectory+aGenFragment)
    dumpProcess(process, "PSet.py")

    prepareCrabCfg(workAreaName, eventsPerJob, numberOfJobs,
                  outLFNDirBase, storage_element, 
                  requestName, outputDatasetTag)

    if not runLocal:
        os.system("crab submit -c crabTmp.py")
        os.system("rm -f PSet.py* crabTmp.py*")      
#######################################################