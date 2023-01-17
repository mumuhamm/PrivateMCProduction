import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter(
    "Pythia8PtGun",

    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),

    comEnergy = cms.double(13000), 
    SLHAFileForPythia8 = cms.string('Configuration/Generator/data/HSCP_stop_400_SLHA.spc'), 

    hscpFlavor = cms.untracked.string('stop'),
    massPoint = cms.untracked.int32(400),
    particleFile = cms.untracked.string('Configuration/Generator/data/particles_stop_400_GeV.txt'),
    slhaFile = cms.untracked.string('Configuration/Generator/data/HSCP_stop_400_SLHA.spc'),
    processFile = cms.untracked.string('SimG4Core/CustomPhysics/data/stophadronProcessList.txt'),
    pdtFile = cms.FileInPath('Configuration/Generator/data/hscppythiapdtstop400.tbl'),
    useregge = cms.bool(False),

    PGunParameters = cms.PSet(
        ParticleID = cms.vint32(1000006),
        AddAntiParticle = cms.bool(True),
        MinPhi = cms.double(-3.14159265359),
        MaxPhi = cms.double(3.14159265359),
        MinPt = cms.double(1.0),
        MaxPt = cms.double(100.0),
        MinEta = cms.double(-2.4),
        MaxEta = cms.double(2.4)
        ),

    PythiaParameters = cms.PSet(
        parameterSets = cms.vstring()
         )
)

