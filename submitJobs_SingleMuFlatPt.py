#!/usr/bin/env python3

import os

from python.utilityFunctions import *
#########################################
#########################################
genFragmentsDirectory = "Configuration/GenProduction/python/GenFragments/"
generator_fragment=genFragmentsDirectory+"DoubleMuPt1to100Eta24_cfi.py"

era = "Run2029"
workAreaName = "tasks_SingleMuFlatPt"
eventsPerJob = 8000
numberOfJobs = 100
outLFNDirBase = "/store/user/akalinow/Data/SingleMu/"
#storage_element="T2_PL_Swierk"
storage_element="T3_CH_CERNBOX"
outputDatasetTag = "12_5_2_p1_15_02_2023"
withPileUp = False
withReco = False
runLocal = False
turnOffG4Secondary = False

iPtTest = 0 
signTest = -1
etaRange = (-2.5,2.5)
#########################################
#########################################
for iPt in range(0,3):
    for sign in range(-1,1,2):

        if iPtTest!=None and signTest!=None and (iPt!=iPtTest or sign!=signTest):
            continue  

        requestName = "SingleMu_ch"+str(sign+1)+"_iPt"+str(iPt)+"_"+outputDatasetTag

        process = runCMSDriver(era, withPileUp, withReco, generator_fragment)
        process = adaptGunParameters(process, iPt, sign, etaRange, turnOffG4Secondary)
        dumpProcess(process, "PSet.py")

        prepareCrabCfg(workAreaName, eventsPerJob, numberOfJobs,
                    outLFNDirBase, storage_element, 
                    requestName, outputDatasetTag)

        if not runLocal:
            os.system("crab submit -c crabTmp.py")
            os.system("rm -f PSet.py* crabTmp.py*")                  
########################################################
