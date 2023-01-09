#!/usr/bin/env python3

import os

from python.utilityFunctions import *
#########################################
#########################################
genFragmentsDirectory = "Configuration/GenProduction/python/GenFragments/"
generator_fragment=genFragmentsDirectory+"DoubleStop400_Pt1to100Eta24_cfi.py"

era = "Run2029"
workAreaName = "tasks_SingleHSCPFlatPt"
eventsPerJob = 100
numberOfJobs = 10
outLFNDirBase = "/store/user/akalinow/OMTF/"
storage_element="T2_PL_Swierk"
outputDatasetTag = "test_09_01_2023"
withPileUp = False
runLocal = True

turnOffG4Secondary = True

iPtTest = 0 
signTest = -1
etaRange = (-3,3)
masses = [100, 200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400, 2600]

mass = 100
#########################################
#########################################
for iPt in range(0,3):
    for sign in range(-1,1,2):

        if iPt!=iPtTest or sign!=signTest:
            continue  

        requestName = "SingleStop_ch"+str(sign+1)+"_iPt"+str(iPt)+"_"+outputDatasetTag

        process = runCMSDriver(era, withPileUp, generator_fragment)
        process = adaptGunParameters(process, iPt, sign, etaRange, turnOffG4Secondary)
        process = adaptStopGunParameters(process, mass)
        dumpProcess(process, "PSet.py")

        prepareCrabCfg(workAreaName, eventsPerJob, numberOfJobs,
                    outLFNDirBase, storage_element, 
                    requestName, outputDatasetTag)

        if not runLocal:
            os.system("crab submit --dryrun -c crabTmp.py")
            os.system("rm -f PSet.py* crabTmp.py*")                  
########################################################