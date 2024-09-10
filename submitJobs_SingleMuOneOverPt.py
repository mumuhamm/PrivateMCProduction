#!/usr/bin/env python3

import os

from python.utilityFunctions import *
#########################################
#########################################
genFragmentsDirectory = "Configuration/GenProduction/python/GenFragments/"
generator_fragment=genFragmentsDirectory+"DoubleMuOneOverPt1to100Eta24_cfi.py"

era = "Run2029"
workAreaName = "tasks_SingleMuOneOverPt_GPExtrapolation2024"
eventsPerJob = 4000
numberOfJobs = 1000
#outLFNDirBase ="/store/user/akalinow/Data/SingleMu/"
outLFNDirBase = "/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/"
#outLFNDirBase = "/store/user/almuhamm/"
storage_element="T2_CH_CERN"
outputDatasetTag = "13_1_0_03_04_2024"
withPileUp = False
withReco = False
runLocal = False

turnOffG4Secondary = False

signTest = None
etaRange = (-2.5,2.5)
#etaRange = (0.8,1.35)
#etaRange = (-1.35,-0.8)
#etaRange = (-3.0, 3.0)
#########################################
#########################################
for sign in range(-1,2,2):

    #if signTest!=None and sign!=signTest:
    #    continue  

    requestName = "SingleMu_ch"+str(sign+1)+"_OneOverPt"+"_"+era+"_"+outputDatasetTag

    process = runCMSDriver(era, withPileUp, withReco, generator_fragment)
    process = adaptGunParameters(process, -1, sign, etaRange, turnOffG4Secondary)
    dumpProcess(process, "PSet.py")

    prepareCrabCfg(workAreaName, eventsPerJob, numberOfJobs,
                    outLFNDirBase, storage_element, 
                    requestName, outputDatasetTag)

    if not runLocal:
        os.system("crab submit -c crabTmp.py")
        os.system("rm -f PSet.py* crabTmp.py*")                
########################################################

