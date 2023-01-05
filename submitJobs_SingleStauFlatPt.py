#!/usr/bin/env python3

import os

from python.utilityFunctions import *
#########################################
#########################################
genFragmentsDirectory = "Configuration/GenProduction/python/GenFragments/"
generator_fragment=genFragmentsDirectory+"DoubleStau432_Pt1to100Eta24_cfi.py"

era = "Run2029"
workAreaName = "tasks_SingleHSCPFlatPt"
eventsPerJob = 100
numberOfJobs = 10
outLFNDirBase = "/store/user/akalinow/OMTF/"
storage_element="T2_PL_Swierk"
outputDatasetTag = "test_05_01_2023"
withPileUp = False
runLocal = True

turnOffG4Secondary = True

iPtTest = 0 
signTest = -1
etaRange = (-3,3)
masses = [100, 126, 156, 200, 247, 300, 308, 370, 400, 432, 494, 500, 530, 557, 570, 590, 595, \
          600, 605, 610, 620, 651, 700, 730, 745, 770, 790, 795, 800, 805, 810, 820, 871, 900, \
          1000, 1029, 1218, 1409, 1599]

mass = 432
#########################################
#########################################
for iPt in range(0,3):
    for sign in range(-1,1,2):

        if iPt!=iPtTest or sign!=signTest:
            continue  

        requestName = "SingleStau_ch"+str(sign+1)+"_iPt"+str(iPt)+"_"+outputDatasetTag

        process = runCMSDriver(era, withPileUp, generator_fragment)
        process = adaptGunParameters(process, iPt, sign, etaRange, turnOffG4Secondary)
        process = adaptStauGunParameters(process, mass)
        dumpProcess(process, "PSet.py")

        prepareCrabCfg(workAreaName, eventsPerJob, numberOfJobs,
                    outLFNDirBase, storage_element, 
                    requestName, outputDatasetTag)

        if not runLocal:
            os.system("crab submit --dryrun -c crabTmp.py")
            os.system("rm -f PSet.py* crabTmp.py*")                  
########################################################