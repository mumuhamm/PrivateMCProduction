import FWCore.ParameterSet.Config as cms

generator = cms.EDFilter("Pythia8PtGun",
    PGunParameters = cms.PSet(
        AddAntiParticle = cms.bool(True),
        MaxEta = cms.double(1.4),
        MaxPhi = cms.double(3.14159265359),
        MaxPt = cms.double(200.0),
        MinEta = cms.double(-1.4),
        MinPhi = cms.double(-3.14159265359),
        MinPt = cms.double(10.0),
        ParticleID = cms.vint32(111)
    ),
    PythiaParameters = cms.PSet(
        parameterSets = cms.vstring('processParameters'),
        processParameters = cms.vstring(
            '111:onMode = off',
            '111:onIfMatch = 22 22')
    ),
    Verbosity = cms.untracked.int32(0),
    firstRun = cms.untracked.uint32(1),
    maxEventsToPrint = cms.untracked.int32(1),
    psethack = cms.string('double pi0 pt'),
    pythiaHepMCVerbosity = cms.untracked.bool(True),
    pythiaPylistVerbosity = cms.untracked.int32(1)
)

