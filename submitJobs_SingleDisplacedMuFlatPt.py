#!/usr/bin/env python3

import os

from python.utilityFunctions import *
#########################################
#########################################
genFragmentsDirectory = "Configuration/GenProduction/python/GenFragments/"
generator_fragment=genFragmentsDirectory+"DoubleDisplacedMuPt1to100Eta24Dxy0to100_cfi.py"

era = "Run2029"
workAreaName = "tasks_SingleDisplacedMuFlatPt_Dxy5m_RunPhaseII_EtaMod3"
eventsPerJob = 5000
numberOfJobs = 400
outLFNDirBase = "/store/group/dpg_trigger/comm_trigger/L1Trigger/OMTF/"
storage_element="T2_CH_CERN"
outputDatasetTag = "14_1_0pre4_11_06_2024_Dxy5m_Run3"
withPileUp = False
withReco = False
runLocal = False

turnOffG4Secondary = False

iPtTest = None
signTest = None
etaRange = (-3,3)
##NOTE: displacement expressed in mm
dxyRange = (0,5000)
LxyMax = 8000
LzMax = 8000
#########################################
#########################################
for iPt in range(0,3):
    for sign in range(-1,2,2):

        #if iPtTest!=None and signTest!=None and (iPt!=iPtTest or sign!=signTest):
           # continue 

        requestName = "DisplacedMu_ch"+str(sign+1)+"_iPt"+str(iPt)+"_"+era+"_"+outputDatasetTag
        print("And this is where I am printing the request name : =================:     ", requestName)
        process = runCMSDriver(era, withPileUp, withReco, generator_fragment)
        process = adaptGunParameters(process, iPt, sign, etaRange, turnOffG4Secondary, 
                                    dxyRange=dxyRange, LxyMax=LxyMax, LzMax=LzMax)

        dumpProcess(process, "PSet.py")

        prepareCrabCfg(workAreaName, eventsPerJob, numberOfJobs,
                    outLFNDirBase, storage_element, 
                    requestName, outputDatasetTag)

        if not runLocal:
            os.system("crab submit -c crabTmp.py")
            os.system("rm -f PSet.py* crabTmp.py*")                  
########################################################
