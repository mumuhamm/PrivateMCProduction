import os, math, glob
from termcolor import colored

import FWCore.ParameterSet.Config as cms

from crab3 import *
#########################################
#########################################
pileup_inputs = {
    "Run2029":" ",
    }
#########################################
#########################################
eras_conditions = {
    "Run2029":"--era Phase2C17I13M9  --conditions 125X_mcRun4_realistic_v2 --geometry Extended2026D88",
    }
#########################################
#########################################
def runCMSDriver(era, withPileUp, withReco, generator_fragment):

    # cmsDriver configuration based on following MC request:
    # https://cms-pdmv.cern.ch/mcm/requests?dataset_name=DYToLL_M-10To50_TuneCP5_14TeV-pythia8&page=0&shown=127
    
   
    # cmsDriver configuration based on following MC request:
    #GEN_SIM: 
    #https://cms-pdmv.cern.ch/mcm/requests?prepid=TSG-Phase2Fall22GS-00004
    #
    #DIGI-RECO
    #https://cms-pdmv.cern.ch/mcm/requests?prepid=TSG-Phase2Fall22DRMiniAOD-00060

# cmsDriver command
    CMSSW_BASE = os.environ.get("CMSSW_BASE")
    command = "ln -s ${PWD}/GenFragments "+ CMSSW_BASE+"/src/Configuration/GenProduction/python/"
    os.system(command)
    
    
    premix_switches = "--step GEN,SIM,DIGI,L1"
    if withReco:
        premix_switches += ",DIGI2RAW,HLT:@fake2,RAW2DIGI,RECO,RECOSIM "
    else:
        premix_switches += " "
    if withPileUp:
         premix_switches = premix_switches.replace("DIGI","DIGI,DATAMIX")
         premix_switches += pileup_inputs[era]+" "
         premix_switches += "--procModifiers premix_stage2 --datamix PreMix "

    if era=="Run2029":
        premix_switches = premix_switches.replace("DIGI,L1","DIGI,L1TrackTrigger,L1")
        premix_switches += "--beamspot HLLHC14TeV "
        premix_switches += "--customise SLHCUpgradeSimulations/Configuration/aging.customise_aging_1000 "
        premix_switches += "--customise L1Trigger/Configuration/customisePhase2TTOn110.customisePhase2TTOn110 "
        premix_switches += "--customise Configuration/DataProcessing/Utils.addMonitoring "
        premix_switches += "--customise UserCode/OmtfAnalysis/privateCustomizations.customize_L1TkMuonsGmt "
        premix_switches += "--customise UserCode/OmtfAnalysis/privateCustomizations.customize_outputCommands "
              
    if withReco:
        premix_switches += "--customise UserCode/OmtfAnalysis/privateCustomizations.customize_extra_outputCommands " 

    command = "cmsDriver.py " 
    command += generator_fragment+" "
    command += "--processName fullsim " 
    command += "--fileout file:FEVTSIM.root " 
    command += "--mc --eventcontent FEVTSIM "
    command += premix_switches 
    command += eras_conditions[era] +" "
    command += "--nThreads 1 "
    command += "--python_filename PSet.py -n 2 --no_exec "    

    if generator_fragment.find("DoubleMu")==-1 and generator_fragment.find("DoubleDisplacedMu")==-1:
        command += "--customise SimG4Core/CustomPhysics/Exotica_HSCP_SIM_cfi.customise "

    print(colored("cmsDriver command:\n","blue"),command)
    os.system(command)
    from PSet import process
    return process
#########################################
#########################################
def adaptGunParameters(process, iPt, sign, etaRange, turnOffG4Secondary, dxyRange=None):

    chargeNames = ["m", "", "p"]
    pdgIdMap = {"mu":13, "stau":1000015, "stop":1000006}

    if iPt>-1:
        ptRanges = [1, 10, 100, 1000]
        process.source.firstRun = cms.untracked.uint32(iPt+1)
        process.generator.PGunParameters.MinPt = ptRanges[iPt]
        process.generator.PGunParameters.MaxPt = ptRanges[iPt+1]
        fileName = "iPt_"+str(iPt)+"_"+chargeNames[sign+1]
        process.FEVTSIMoutput.fileName =  'SingleMu'+"_"+fileName+'.root'
    else:
        process.source.firstRun = cms.untracked.uint32(1)
        process.generator.PGunParameters.MinOneOverPt = 1.0/100.0
        process.generator.PGunParameters.MaxOneOverPt = 1.0/1.5
        fileName = "OneOverPt_1_100_"+chargeNames[sign+1]
        process.FEVTSIMoutput.fileName =  'SingleMu'+"_"+fileName+'.root'
    if hasattr(process.generator.PGunParameters, "PartID"): #HepMC guns
        process.generator.PGunParameters.PartID = [-sign*13] #muon assumed for HepMC gun
    elif hasattr(process.generator.PGunParameters, "ParticleID"): #Py8 guns
        process.generator.PGunParameters.ParticleID = [-sign*13] #muon
        if hasattr(process.generator, "hscpFlavor"):
            process.generator.PGunParameters.ParticleID = [-sign*pdgIdMap[process.generator.hscpFlavor.value()]]
    process.generator.PGunParameters.MinPhi = -math.pi
    process.generator.PGunParameters.MaxPhi = math.pi
    process.generator.PGunParameters.MinEta = etaRange[0]
    process.generator.PGunParameters.MaxEta = etaRange[1]
    if hasattr(process.generator, "AddAntiParticle"): #HepMC guns
        process.generator.AddAntiParticle = False
    elif hasattr(process.generator.PGunParameters, "AddAntiParticle"): #Py8 guns
        process.generator.PGunParameters.AddAntiParticle = False
    if dxyRange != None:
        #set displacement
        process.generator.PGunParameters.dxyMin = dxyRange[0]
        process.generator.PGunParameters.dxyMax = dxyRange[1]
        process.FEVTSIMoutput.fileName = 'Displaced'+process.FEVTSIMoutput.fileName.value()

    if turnOffG4Secondary:
        print(colored("Switching off secondaries in G4","red"))
        process.g4SimHits.StackingAction.KillDeltaRay = True
        process.g4SimHits.StackingAction.KillGamma = True
        process.g4SimHits.StackingAction.KillHeavy = True
        process.g4SimHits.StackingAction.GammaThreshold = 1E9
        process.g4SimHits.StackingAction.SaveAllPrimaryDecayProductsAndConversions = False

    return process
#########################################
#########################################
def adaptStauGunParameters(process, mass):
    
    mass = str(mass)
    process.FEVTSIMoutput.fileName = process.FEVTSIMoutput.fileName.value().replace('Mu','Stau'+mass)
    process.customPhysicsSetup.particlesDef = process.customPhysicsSetup.particlesDef.value().replace('432',mass)
    process.generator.SLHAFileForPythia8 = process.generator.SLHAFileForPythia8.value().replace('432',mass)
    process.generator.massPoint = int(mass)
    process.generator.particleFile = process.generator.particleFile.value().replace('432',mass)
    process.generator.pdtFile = process.generator.pdtFile.value().replace('432',mass)
    process.generator.slhaFile = process.generator.slhaFile.value().replace('432',mass)
    process.customPhysicsSetup.particlesDef = process.customPhysicsSetup.particlesDef.value().replace('432',mass)
    process.g4SimHits.Physics.particlesDef = process.g4SimHits.Physics.particlesDef.value().replace('432',mass)
    return process

#########################################
#########################################
def adaptStopGunParameters(process, mass):
    
    mass = str(mass)
    process.FEVTSIMoutput.fileName = process.FEVTSIMoutput.fileName.value().replace('Mu','Stop'+mass)
    process.customPhysicsSetup.particlesDef = process.customPhysicsSetup.particlesDef.value().replace('400',mass)
    process.generator.SLHAFileForPythia8 = process.generator.SLHAFileForPythia8.value().replace('400',mass)
    process.generator.massPoint = int(mass)
    process.generator.particleFile = process.generator.particleFile.value().replace('400',mass)
    process.generator.pdtFile = process.generator.pdtFile.value().replace('400',mass)
    process.generator.slhaFile = process.generator.slhaFile.value().replace('400',mass)
    process.customPhysicsSetup.particlesDef = process.customPhysicsSetup.particlesDef.value().replace('400',mass)
    process.g4SimHits.Physics.particlesDef = process.g4SimHits.Physics.particlesDef.value().replace('400',mass)
    return process 
#########################################
#########################################
def dumpProcess(process, fileName):

    process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

    out = open(fileName,'w')
    out.write(process.dumpPython())
    out.close()
#########################################
#########################################
def prepareCrabCfg(workAreaName,
                   eventsPerJob,
                   numberOfJobs,
                   outLFNDirBase,
                   storage_element,
                   requestName,
                   outputDatasetTag):
    
    outputPrimaryDataset = requestName
    print(colored("requestName:","blue"),requestName)          
    print(colored("outputPrimaryDataset:","blue"),outputPrimaryDataset)
    print(colored("outputDatasetTag:","blue"),outputDatasetTag)

    ##Modify CRAB3 configuration
    config.JobType.allowUndistributedCMSSW = True
    config.JobType.pluginName = 'PrivateMC'
    config.JobType.psetName = 'PSet.py'
    config.JobType.numCores = 1
    config.JobType.maxMemoryMB = 3000
    
    config.General.requestName = requestName
    config.General.workArea = workAreaName
    
    config.Data.inputDataset = None
    config.Data.outLFNDirBase = outLFNDirBase+outputDatasetTag
    config.Data.publication = True
    config.Data.outputPrimaryDataset = outputPrimaryDataset
    config.Data.outputDatasetTag = outputDatasetTag

    config.Site.storageSite = storage_element
    
    config.Data.unitsPerJob = eventsPerJob
    config.Data.totalUnits = eventsPerJob*numberOfJobs

    fullWorkDirName = config.General.workArea+"/crab_"+config.General.requestName
    requestExists = len(glob.glob(fullWorkDirName))!=0
    if requestExists:
        print(colored("Request with name: {} exists. Skipping.".format(fullWorkDirName), "red"))
        return

    out = open('crabTmp.py','w')
    out.write(config.pythonise_())
    out.close()    
#########################################
#########################################
