#!/usr/bin/env python3

import os

from python.utilityFunctions import *
#########################################
#########################################
genFragmentsDirectory = "Configuration/GenProduction/python/GenFragments/"
generator_fragment=genFragmentsDirectory+"DoubleDisplacedMuPt1to100Eta24Dxy0to100_cfi.py"

era = "Run2029"
workAreaName = "tasks_SingleDisplacedMuFlatPt"
eventsPerJob = 5000
numberOfJobs = 10
outLFNDirBase = "/store/user/akalinow/Data/SingleMu/"
storage_element="T3_CH_CERNBOX"
outputDatasetTag = "13_1_0_03_10_2023"
withPileUp = False
withReco = False
runLocal = True

turnOffG4Secondary = False

iPtTest = 0
signTest = 1
etaRange = (0.8,2.0)
##NOTE: displacement expressed in mm
dxyRange = (0,100)
LxyMax = 200
LzMax = 100
#########################################
#########################################
for iPt in range(0,3):
    for sign in range(-1,2,2):

        if iPtTest!=None and signTest!=None and (iPt!=iPtTest or sign!=signTest):
            continue 

        requestName = "DisplacedMu_ch"+str(sign+1)+"_iPt"+str(iPt)+"_"+era+"_"+outputDatasetTag

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
